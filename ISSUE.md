# Post-Fix Audit — Remaining Issues

> **Date:** 2026-09-17 | **Status:** 🔴 New findings after original 11 fixes | **Issues found:** 10

---

## 🔴 HIGH — Will Cause Wrong Behaviour / Crash

### Issue A — `Whisper.py` L51: `raise RuntimeError(f"...", e)` — **silently drops the exception**

`RuntimeError(message, e)` creates a 2-arg tuple as `args` — the original exception `e` is **not chained** and its traceback is lost. Also the message contains a typo: `"Exeption"`.

```python
# ❌ Wrong — e is passed as a second positional arg, not chained
raise RuntimeError(f"Exeption in {self.__class__.__name__}", e)

# ✅ Right — chain properly and fix typo
raise RuntimeError(f"Exception in {self.__class__.__name__}") from e
```

Also affects L34 where the same typo `"Exeption"` appears in an f-string.

**Files:** [`embedder/Whisper.py`](file:///workspaces/codespaces-blank/voice-changer/server/voice_changer/RVC/embedder/Whisper.py) L34, L51

---

### Issue B — `OnnxContentvec.py` raises generic `Exception` (not `NotImplementedError`)

Both `loadModel()` and `extractFeatures()` raise `Exception("Not implemented")` which is caught by **every** `except Exception as e:` block in the call stack, silently swallowing it as a normal runtime error. Should raise `NotImplementedError` so it propagates correctly.

```python
# ❌  raise Exception("Not implemented")
# ✅  raise NotImplementedError("OnnxContentvec is not implemented")
```

**File:** [`embedder/OnnxContentvec.py`](file:///workspaces/codespaces-blank/voice-changer/server/voice_changer/RVC/embedder/OnnxContentvec.py)

---

## ⚠️ MEDIUM — Fix Before Deploying

### Issue C — Resource leaks: 4× `open()` without `with` statement

File handles opened inline in `json.load(open(...))` / `json.dump(..., open(...))` are **never explicitly closed**. On CPython the GC closes them eventually, but on PyPy or under load this leaks OS file descriptors. Also two of these calls are missing `encoding="utf-8"`.

| File | Line | Problem |
|---|---|---|
| [`VoiceChangerManager.py`](file:///workspaces/codespaces-blank/voice-changer/server/voice_changer/VoiceChangerManager.py#L112) | 112 | `open(FILE, "w")` — no `with`, no `encoding` |
| [`ModelSlot.py`](file:///workspaces/codespaces-blank/voice-changer/server/data/ModelSlot.py#L54) | 54 | `open(jsonFile)` — no `with` (has `encoding`) |
| [`ModelSlot.py`](file:///workspaces/codespaces-blank/voice-changer/server/data/ModelSlot.py#L79) | 79 | `open(path, "w")` — no `with`, no `encoding` |

```python
# ❌  json.dump(data, open(FILE, "w"))
# ✅  with open(FILE, "w", encoding="utf-8") as f:
#        json.dump(data, f)
```

---

### Issue D — `VoiceChangerManager.py` L84: `threading.Thread` missing `daemon=True`

The `ServerDevice` thread is started without `daemon=True`. If the main process exits or crashes, this thread **blocks shutdown** indefinitely, keeping the process alive.

```python
# ❌
thread = threading.Thread(target=self.serverDevice.start, args=())
thread.start()

# ✅
thread = threading.Thread(target=self.serverDevice.start, args=(), daemon=True)
thread.start()
```

**File:** [`VoiceChangerManager.py`](file:///workspaces/codespaces-blank/voice-changer/server/voice_changer/VoiceChangerManager.py#L84)

---

### Issue E — `VoiceChangerManager.py` L231: bare `except:` catches `KeyboardInterrupt` / `SystemExit`

The bare `except:` inside the `modelSlotIndex` parse block will silently swallow `KeyboardInterrupt` and `SystemExit` — prevents clean shutdown. Should be `except (ValueError, TypeError):`.

```python
# ❌  except:
# ✅  except (ValueError, TypeError):
```

**File:** [`VoiceChangerManager.py`](file:///workspaces/codespaces-blank/voice-changer/server/voice_changer/VoiceChangerManager.py#L231)

---

### Issue F — `PipelineGenerator.py` L72: bare `except:` on faiss index load

Same problem — bare `except: # NOQA` catches `KeyboardInterrupt` / `SystemExit`. Should be `except Exception:`.

```python
# ❌  except: # NOQA
# ✅  except Exception:  # noqa: BLE001
```

**File:** [`pipeline/PipelineGenerator.py`](file:///workspaces/codespaces-blank/voice-changer/server/voice_changer/RVC/pipeline/PipelineGenerator.py#L72)

---

### Issue G — `ModelSlotManager.py` L69: `logger.error(e)` loses traceback

`logger.error(e)` only logs the exception string, dropping the full traceback. Should use `logger.exception(e)` (or `logger.error(e, exc_info=True)`) so the stack trace appears in logs.

```python
# ❌  logger.error(e)
# ✅  logger.exception(e)
```

**File:** [`ModelSlotManager.py`](file:///workspaces/codespaces-blank/voice-changer/server/voice_changer/ModelSlotManager.py#L69)

---

## 🟡 LOW — Cleanup

### Issue H — `voras_beta/config.py`: `from typing import *` star import

Pollutes the module namespace. All types actually used (`List`, `Dict`, `Optional`, `Literal`, `Any`) should be imported explicitly. On Python ≥3.9 the built-in `list`, `dict`, `tuple` can replace `List`, `Dict`, `Tuple`.

```python
# ❌  from typing import *
# ✅  from typing import Any, Dict, List, Literal, Optional
```

**File:** [`inferencer/voras_beta/config.py`](file:///workspaces/codespaces-blank/voice-changer/server/voice_changer/RVC/inferencer/voras_beta/config.py#L1)

---

### Issue I — `RVCr2.py` L303: hardcoded `/tmp/` in export path returned to client

```python
"path": f"/tmp/{output_file_simple}",
```

This hardcodes the OS temp directory in the HTTP response. On Windows (or custom temp configs) this path will be wrong. Should use `TMP_DIR` constant already defined in `const.py`.

**File:** [`RVC/RVCr2.py`](file:///workspaces/codespaces-blank/voice-changer/server/voice_changer/RVC/RVCr2.py#L303)

---

### Issue J — `MMVC_Namespace.py` L22: `asyncio.run()` inside a sync method called from an async context

`emit_coroutine()` calls `asyncio.run(self.emitTo(data))` but `emitTo` is an `async` method and `asyncio.run()` creates a **new event loop** — calling it from within a running event loop (uvicorn's) will raise `RuntimeError: This event loop is already running`.

The method is already commented out in `__init__` (`# self.voiceChangerManager.voiceChanger.emitTo = self.emit_coroutine`) but `emit_coroutine` still exists as dead code. Should be removed or replaced with a proper async approach.

**File:** [`sio/MMVC_Namespace.py`](file:///workspaces/codespaces-blank/voice-changer/server/sio/MMVC_Namespace.py#L22)

---

## Fix Priority Order

```
A. Whisper.py raise RuntimeError(msg, e) → raise ... from e  + typo fix
B. OnnxContentvec.py Exception → NotImplementedError
C. open() resource leaks (4 locations) + missing encoding
D. threading.Thread daemon=True
E. bare except: in VoiceChangerManager → except (ValueError, TypeError):
F. bare except: in PipelineGenerator → except Exception:
G. logger.error(e) → logger.exception(e) in ModelSlotManager
H. voras_beta/config.py star import → explicit imports
I. /tmp hardcoded path in RVCr2.py
J. asyncio.run dead code in MMVC_Namespace.py
```
