import React, { useEffect, useMemo, useRef, useState } from "react";
import { useAppState } from "../../001_provider/001_AppStateProvider";
import { ModelFileKind, ModelUploadSetting, fileSelector } from "@dannadori/voice-changer-client-js";
import { useMessageBuilder } from "../../hooks/useMessageBuilder";
import { ModelSlotManagerDialogScreen } from "./904_ModelSlotManagerDialog";
import { checkExtention, trimfileName } from "../../utils/utils";

export type FileUploaderScreenProps = {
    screen: ModelSlotManagerDialogScreen;
    targetIndex: number;
    close: () => void;
    backToSlotManager: () => void;
};

type SubScreen = "FileUploader" | "URLUploader";

export const FileUploaderScreen = (props: FileUploaderScreenProps) => {
    const { serverSetting } = useAppState();
    // Always RVC — the VoiceChangerType dropdown has been removed
    const voiceChangerType = "RVC";
    const [uploadSetting, setUploadSetting] = useState<ModelUploadSetting>();
    const messageBuilderState = useMessageBuilder();

    // URL uploader state
    const [subScreen, setSubScreen] = useState<SubScreen>("FileUploader");
    const [urlInput, setUrlInput] = useState<string>("");
    const [urlUploadStatus, setUrlUploadStatus] = useState<"idle" | "downloading">("idle");
    const [urlProgress, setUrlProgress] = useState<number>(0);
    const [urlError, setUrlError] = useState<string>("");
    const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

    useMemo(() => {
        messageBuilderState.setMessage(__filename, "header_message", { ja: "ファイルをアップロードしてください. 対象：", en: "Upload Files for " });
        messageBuilderState.setMessage(__filename, "back", { ja: "戻る", en: "back" });
        messageBuilderState.setMessage(__filename, "select", { ja: "ファイル選択", en: "select file" });
        messageBuilderState.setMessage(__filename, "upload", { ja: "アップロード", en: "upload" });
        messageBuilderState.setMessage(__filename, "uploading", { ja: "アップロード中", en: "uploading" });
        messageBuilderState.setMessage(__filename, "alert-model-ext", {
            ja: "ファイルの拡張子は次のモノである必要があります。",
            en: "extension of file should be the following.",
        });
        messageBuilderState.setMessage(__filename, "alert-model-file", {
            ja: "ファイルが選択されていません",
            en: "file is not selected.",
        });
    }, []);

    useEffect(() => {
        setUploadSetting({
            voiceChangerType: voiceChangerType,
            slot: props.targetIndex,
            isSampleMode: false,
            sampleId: null,
            files: [],
            params: {},
        });
        // Reset sub-screen when target slot changes
        setSubScreen("FileUploader");
        setUrlInput("");
        setUrlError("");
        setUrlProgress(0);
        setUrlUploadStatus("idle");
    }, [props.targetIndex]);

    // Clear the polling interval when the component unmounts
    useEffect(() => {
        return () => {
            if (pollRef.current !== null) {
                clearInterval(pollRef.current);
            }
        };
    }, []);

    const handleUrlUpload = async () => {
        if (!urlInput.trim()) return;
        setUrlUploadStatus("downloading");
        setUrlProgress(0);
        setUrlError("");
        await serverSetting.downloadModelFromUrl(urlInput.trim(), props.targetIndex);
        pollRef.current = setInterval(async () => {
            const data = await serverSetting.getUrlDownloadStatus(props.targetIndex);
            if (!data) return;
            setUrlProgress(data.progress);
            if (data.status === "done") {
                clearInterval(pollRef.current!);
                pollRef.current = null;
                setUrlUploadStatus("idle");
                await serverSetting.reloadServerInfo();
                props.backToSlotManager();
            } else if (data.status === "error") {
                clearInterval(pollRef.current!);
                pollRef.current = null;
                setUrlUploadStatus("idle");
                setUrlError(data.msg || "An unexpected error occurred. Check server logs.");
            }
        }, 500);
    };


    const screen = useMemo(() => {
        if (props.screen != "FileUploader") {
            return <></>;
        }

        // ── URL Uploader sub-screen ───────────────────────────────────────────
        if (subScreen === "URLUploader") {
            return (
                <div className="dialog-frame">
                    <div className="dialog-title">File Uploader</div>
                    <div className="dialog-fixed-size-content">
                        <div className="file-uploader-header">
                            Upload Model via URL
                            <span
                                onClick={() => {
                                    if (urlUploadStatus !== "downloading") {
                                        setSubScreen("FileUploader");
                                        setUrlError("");
                                    }
                                }}
                                className="file-uploader-header-button"
                            >
                                &lt;&lt;{messageBuilderState.getMessage(__filename, "back")}
                            </span>
                        </div>

                        <div className="file-uploader-file-select-container">
                            <div style={{ marginBottom: "8px", padding: "8px", background: "#f0f4ff", borderRadius: "4px", fontSize: "0.85em" }}>
                                ℹ️ <strong>Supported sources:</strong>
                                <ul style={{ margin: "4px 0 0 16px", padding: 0 }}>
                                    <li>Google Drive</li>
                                    <li>HuggingFace</li>
                                    <li>Pixeldrain</li>
                                </ul>
                            </div>

                            <div className="file-uploader-file-select-row">
                                <div className="file-uploader-file-select-row-label">URL:</div>
                                <input
                                    type="text"
                                    value={urlInput}
                                    onChange={(e) => setUrlInput(e.target.value)}
                                    placeholder="Paste model URL here…"
                                    disabled={urlUploadStatus === "downloading"}
                                    style={{ flex: 1, padding: "4px 8px", borderRadius: "4px", border: "1px solid #ccc" }}
                                />
                            </div>

                            {urlUploadStatus === "downloading" && (
                                <div style={{ marginTop: "12px" }}>
                                    <div style={{ background: "#e0e0e0", borderRadius: "4px", height: "12px", overflow: "hidden" }}>
                                        <div
                                            style={{
                                                background: "#4a90d9",
                                                width: `${urlProgress}%`,
                                                height: "100%",
                                                transition: "width 0.3s",
                                            }}
                                        />
                                    </div>
                                    <div style={{ textAlign: "center", fontSize: "0.85em", marginTop: "4px" }}>
                                        Downloading… {urlProgress}%
                                    </div>
                                </div>
                            )}

                            {urlError && (
                                <div style={{ marginTop: "10px", color: "#c0392b", fontSize: "0.9em" }}>
                                    ❌ Failed: {urlError}
                                </div>
                            )}
                        </div>

                        <div className="file-uploader-file-select-upload-button-container">
                            <div
                                className="file-uploader-file-select-upload-button"
                                onClick={() => {
                                    if (urlUploadStatus !== "downloading") {
                                        handleUrlUpload();
                                    }
                                }}
                            >
                                {urlUploadStatus === "downloading" ? `Downloading… (${urlProgress}%)` : "Upload via URL"}
                            </div>
                        </div>
                    </div>
                </div>
            );
        }

        // ── Main File Uploader screen ─────────────────────────────────────────
        const checkModelSetting = (setting: ModelUploadSetting) => {
            const enough = !!setting.files.find((x) => {
                return x.kind == "rvcModel";
            });
            return enough;
        };

        const generateFileRow = (setting: ModelUploadSetting, title: string, kind: ModelFileKind, ext: string[], dir: string = "") => {
            const selectedFile = setting.files.find((x) => {
                return x.kind == kind;
            });
            const selectedFilename = selectedFile?.file.name || "";
            return (
                <div key={`${title}`} className="file-uploader-file-select-row">
                    <div className="file-uploader-file-select-row-label">{title}:</div>
                    <div className="file-uploader-file-select-row-value">{trimfileName(selectedFilename, 30)}</div>
                    <div
                        className="file-uploader-file-select-row-button"
                        onClick={async () => {
                            const file = await fileSelector("");
                            if (checkExtention(file.name, ext) == false) {
                                const alertMessage = `${messageBuilderState.getMessage(__filename, "alert-model-ext")} ${ext}`;
                                alert(alertMessage);
                                return;
                            }
                            if (selectedFile) {
                                selectedFile.file = file;
                            } else {
                                setting.files.push({ kind: kind, file: file, dir: dir });
                            }
                            setUploadSetting({ ...setting });
                        }}
                    >
                        {messageBuilderState.getMessage(__filename, "select")}
                    </div>
                </div>
            );
        };

        const fileRows = [
            generateFileRow(uploadSetting!, "Model", "rvcModel", ["pth", "onnx"]),
            generateFileRow(uploadSetting!, "Index", "rvcIndex", ["index", "bin"]),
        ];

        const buttonLabel =
            serverSetting.uploadProgress == 0
                ? messageBuilderState.getMessage(__filename, "upload")
                : messageBuilderState.getMessage(__filename, "uploading") + `(${serverSetting.uploadProgress.toFixed(1)}%)`;

        return (
            <div className="dialog-frame">
                <div className="dialog-title">File Uploader</div>
                <div className="dialog-fixed-size-content">
                    <div className="file-uploader-header">
                        {messageBuilderState.getMessage(__filename, "header_message")} Slot[{props.targetIndex}]
                        <span
                            onClick={() => {
                                props.backToSlotManager();
                            }}
                            className="file-uploader-header-button"
                        >
                            &lt;&lt;{messageBuilderState.getMessage(__filename, "back")}
                        </span>
                    </div>

                    <div className="file-uploader-file-select-container">{fileRows}</div>
                    <div className="file-uploader-file-select-upload-button-container">
                        <div
                            className="file-uploader-file-select-upload-button"
                            onClick={() => {
                                if (!uploadSetting) {
                                    return;
                                }
                                if (serverSetting.uploadProgress != 0) {
                                    return;
                                }
                                if (checkModelSetting(uploadSetting)) {
                                    serverSetting.uploadModel(uploadSetting).then(() => {
                                        props.backToSlotManager();
                                    });
                                } else {
                                    const errorMessage = messageBuilderState.getMessage(__filename, "alert-model-file");
                                    alert(errorMessage);
                                }
                            }}
                        >
                            {buttonLabel}
                        </div>
                        <div
                            className="file-uploader-file-select-upload-button"
                            onClick={() => {
                                setSubScreen("URLUploader");
                                setUrlError("");
                            }}
                            style={{ marginTop: "8px" }}
                        >
                            Upload Model via URL
                        </div>
                    </div>
                </div>
            </div>
        );
    }, [props.screen, props.targetIndex, uploadSetting, serverSetting.uploadModel, serverSetting.uploadProgress, subScreen, urlInput, urlUploadStatus, urlProgress, urlError]);

    return screen;
};
