# Graph Report - voice-changer  (2026-09-02)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 5755 nodes · 13159 edges · 248 communities (177 shown, 48 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 834 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- index.js
- i
- c
- e
- DeviceManager
- VoiceChangerManager
- ko
- Timer2
- VoiceChangerParams
- MMVCv15
- EnumInferenceTypes
- n
- s
- he
- devDependencies
- log_control.py
- infer_pack/models.py
- R
- a
- hifigan/models.py
- ft
- ho
- VoiceChangerManager.py
- c
- dependencies
- diffusion_svc_model/nsf_hifigan/models.py
- p
- D
- infer_pack/modules.py
- .updateRemoteVideosFromLastVideosToReceive
- useAppState
- SiFiGANGenerator
- ddsp/pcmer.py
- naive/pcmer.py
- MMVCv13/models/models.py
- hubert/model.py
- devDependencies
- DPM_Solver
- VoiceChangerModel
- VoiceChangerClient
- tools.py
- whisper/model.py
- MultiHeadAttention
- lib/src/const.ts
- diffusion_onnx.py
- 001_GuiStateProvider.tsx
- useClient.ts
- Embedder
- SoVitsSvc40.py
- SoVitsSvc40/models/models.py
- modules/modules.py
- join
- AppSettingProvider.tsx
- DPM_Solver
- .__init__
- MMVCv15/models/models.py
- models/utils.py
- AppStateProvider.tsx
- useMessageBuilder
- useAppSetting
- load_model_vocoder_from_combo
- .__init__
- DiffusionSVC
- MultiHeadAttention
- t
- UniPC
- Conv2d
- package.json
- 207-1MelSpectrogramUtil.ts
- scripts
- .of
- GaussianDiffusion
- ServerDevice
- useAppRoot
- ddsp/vocoder.py
- .__init__
- infer_pack/commons.py
- dependencies
- HParams
- GaussianDiffusion
- NoiseScheduleVP
- NsfHifiGAN
- voras_beta/commons.py
- CrepePitchExtractor
- useGuiState
- scripts
- ddsp/core.py
- models/diffusion/unit2mel.py
- .__init__
- .run
- TorchCrepe2.py
- demo/src/const.ts
- useServerSetting.ts
- VoiceChangerWorkletNode
- compilerOptions
- SvcDDSP.py
- 001_AppStateProvider.tsx
- SynthesizerTrn
- .removeObserver
- .pause
- voras_beta/utils.py
- SnakeFilter
- compilerOptions
- compilerOptions
- LLVC
- useAppState
- compilerOptions
- NoiseScheduleVP
- DiffusionSVC
- modules/commons.py
- MockStream
- recorder/package.json
- models/diffusion/vocoder.py
- models/nsf_hifigan/models.py
- .__init__
- 001_AppRootProvider.tsx
- ServerConfigurator
- ServerRestClient
- Ae
- Resample
- .__init__
- NoiseScheduleVP
- CachedConvNet
- GeneratorVoras
- convert.py
- .chooseInputIntrinsicDevice
- VolumeExtractor
- Conv1d
- DiffusionSVCInferencer
- SignalGenerator
- IMDCTSymExpHead
- webpack_web.common.js
- 100_useFrontendManager.ts
- diffusion_svc_model/DiffusionSVC.py
- filter.py
- threshold.py
- Generator
- 102_ConfigArea.tsx
- demo/webpack.common.js
- VoiceChangerWorkletProcessor
- recorder/webpack.common.js
- Unit2Mel
- EasyVC
- log_mel_spectrogram
- onnxcrepe/core.py
- RVCr2
- ci
- STFT
- SineGen
- llvc.py
- decode.py
- RVC
- vdecoder/nsf_hifigan/nvSTFT.py
- vdecoder/nsf_hifigan/models.py
- SineGen
- node_modules
- webpack.worklet.dev.js
- 002_useDeviceManager.ts
- DiffusionSVC_ONNX
- Net
- PositionalEncoding
- .__init__
- voras_beta/models.py
- mel_processing.py
- hifigan/nvSTFT.py
- BlockingQueue
- index.ts
- BlockingQueue
- lib/webpack.common.js
- AudioDataset
- SSSLoss
- ServerDeviceCallbacks
- WebUIInferencer
- Synthesizer
- AWP
- modules/enhancer.py
- onnxcrepe/__init__.py
- Slicer
- CausalTransformerDecoder
- index_initial
- diffusion_svc_model/diffusion/dpm_solver_pytorch.py
- EmbedderProtocol
- npm-run-all
- .acquireScreenCaptureDisplayInputStream
- je
- DiffGtMel
- .multistep_dpm_solver_update
- UnitsIndexer
- losses.py
- .__init__
- voice-changer-worklet-processor.d.ts
- AttrDict
- Whisper
- voras_beta/transforms.py
- .__init__
- loudness.py
- SpeakerEncoder
- AttrDict
- ts-loader
- @types/react-dom
- webpack-cli
- 010_useMessageBuilder.ts
- tsconfig.worklet.json
- .process
- Volume_Extractor
- .__init__
- solver.py
- DotDict
- buildAllDemo.sh
- build-voice-changer-js.sh
- docker/exec.sh
- docker/setup.sh
- docker_vcclient/exec.sh
- docker_vcclient/setup.sh
- window.d.ts
- 001_pushDocker.sh
- 002_pushDockerTrainer.sh
- 003_pushDockerVCClient.sh
- fillSlot.sh
- initialize.sh
- BeatriceSettings.py
- symbols.py
- start2.sh
- start_docker.sh
- start_v0.1.sh

## God Nodes (most connected - your core abstractions)
1. `i()` - 216 edges
2. `s()` - 181 edges
3. `c()` - 164 edges
4. `n()` - 106 edges
5. `a()` - 103 edges
6. `push()` - 92 edges
7. `e()` - 91 edges
8. `a()` - 91 edges
9. `R` - 90 edges
10. `n()` - 86 edges

## Surprising Connections (you probably didn't know these)
- `TextAudioSpeakerCollate` --uses--> `SignalGenerator`  [INFERRED]
  docker_trainer/scripts/client_modules.py → server/voice_changer/MMVCv15/models/features.py
- `Inferencer` --inherits--> `Protocol`  [EXTRACTED]
  server/voice_changer/DiffusionSVC/inferencer/Inferencer.py → client/lib/src/const.ts
- `Inferencer` --inherits--> `Protocol`  [EXTRACTED]
  server/voice_changer/RVC/inferencer/Inferencer.py → client/lib/src/const.ts
- `ServerDeviceCallbacks` --inherits--> `Protocol`  [EXTRACTED]
  server/voice_changer/Local/ServerDevice.py → client/lib/src/const.ts
- `EmbedderProtocol` --inherits--> `Protocol`  [EXTRACTED]
  server/voice_changer/RVC/embedder/EmbedderProtocol.py → client/lib/src/const.ts

## Import Cycles
- 3-file cycle: `recorder/src/002_hooks/004_useAppStateStorage.ts -> recorder/src/002_hooks/013_useAudioControllerState.ts -> recorder/src/003_provider/AppSettingProvider.tsx -> recorder/src/002_hooks/004_useAppStateStorage.ts`

## Communities (248 total, 48 thin omitted)

### Community 0 - "index.js"
Cohesion: 0.02
Nodes (166): addDeviceChangeObserver(), addObserver(), addToMinuteWindow(), addVideoTile(), applyLocalMuteOverride(), attendeeIdForStreamId(), attendeeIdForTrack(), audioVideoDidStart() (+158 more)

### Community 1 - "i"
Cohesion: 0.02
Nodes (96): t(), acquireAudioInputStream(), addAudioMixObserver(), addEventListener(), an(), t(), asCanvasImageSource(), audioOutputDidChange() (+88 more)

### Community 2 - "c"
Cohesion: 0.02
Nodes (61): ao, Ar(), As, Bs, bt(), concat(), createUrlWithParams(), Cs (+53 more)

### Community 3 - "e"
Cohesion: 0.04
Nodes (61): B, n(), clear(), consume(), o(), e(), d(), I() (+53 more)

### Community 4 - "DeviceManager"
Cohesion: 0.03
Nodes (45): Protocol, DeviceManager, object, CrepeOnnxPitchExtractor, AudioInOut, PitchExtractor, PitchExtractorType, CrepePitchExtractor (+37 more)

### Community 5 - "VoiceChangerManager"
Cohesion: 0.04
Nodes (35): APIRoute, ASGIApp, Receive, Scope, Send, getFrontendPath(), compute_local_origins(), normalize_origins() (+27 more)

### Community 6 - "ko"
Cohesion: 0.04
Nodes (79): ac(), ai, al(), bc(), bl(), bo(), cc(), cl() (+71 more)

### Community 7 - "Timer2"
Cohesion: 0.05
Nodes (30): Exception, DeviceCannotSupportHalfPrecisionException, DeviceChangingException, HalfPrecisionChangingException, NotEnoughDataExtimateF0, ONNXInputArgumentException, PipelineNotInitializedException, VoiceChangerIsNotSelectedException (+22 more)

### Community 8 - "VoiceChangerParams"
Cohesion: 0.05
Nodes (31): DDSPSVCModelSlot, PipelineCreateException, DDSP_SVC, AudioInOut, DDSP_SVCSettings, SvcDDSP, InferencerManager, Pipeline (+23 more)

### Community 9 - "MMVCv15"
Cohesion: 0.04
Nodes (21): MMVCv13ModelSlot, MMVCv15ModelSlot, NoModeLoadedException, MMVCv13, MMVCv13Settings, AudioInOut, get_hparams_from_file(), HParams (+13 more)

### Community 10 - "EnumInferenceTypes"
Cohesion: 0.05
Nodes (34): Enum, EnumInferenceTypes, Inferencer, DiffusionSVCInferenceType, Tensor, EasyVCInferencerONNX, Tensor, Inferencer (+26 more)

### Community 13 - "he"
Cohesion: 0.06
Nodes (3): he, once(), realtimeIsLocalAudioMuted()

### Community 14 - "devDependencies"
Cohesion: 0.04
Nodes (64): @babel/core, devDependencies, autoprefixer, @babel/core, babel-loader, @babel/plugin-transform-runtime, @babel/preset-env, @babel/preset-react (+56 more)

### Community 15 - "log_control.py"
Cohesion: 0.07
Nodes (33): getSampleJsonAndModelIds(), RVCSampleMode, DiffusionSVCModelSample, generateModelSample(), ModelSample, Any, ModelSamples, RVCModelSample (+25 more)

### Community 16 - "infer_pack/models.py"
Cohesion: 0.08
Nodes (13): TextEncoder, Encoder, sequence_mask(), Generator, GeneratorNSF, PosteriorEncoder, ResidualCouplingBlock, SynthesizerTrnMs256NSFsid (+5 more)

### Community 17 - "R"
Cohesion: 0.05
Nodes (5): health(), healthy(), maximumHealth(), minimumHealth(), R

### Community 18 - "a"
Cohesion: 0.05
Nodes (4): a(), localVideoTransceiver(), numberOfParticipants(), numberOfVideoPublishingParticipantsExcludingSelf()

### Community 19 - "hifigan/models.py"
Cohesion: 0.05
Nodes (20): AttrDict, dict, DiscriminatorP, DiscriminatorS, Generator, load_model(), MultiPeriodDiscriminator, MultiScaleDiscriminator (+12 more)

### Community 20 - "ft"
Cohesion: 0.13
Nodes (11): Aa(), ft(), Ma(), qa(), Va(), xa(), za(), c() (+3 more)

### Community 21 - "ho"
Cohesion: 0.07
Nodes (4): co, ho, readyState(), send()

### Community 22 - "VoiceChangerManager.py"
Cohesion: 0.11
Nodes (29): ModelSlot, BeatriceModelSlot, DDSPSVCModelSlot, DiffusionSVCModelSlot, EasyVCModelSlot, LLVCModelSlot, loadSlotInfo(), MMVCv13ModelSlot (+21 more)

### Community 24 - "dependencies"
Cohesion: 0.04
Nodes (49): @alexanderolsen/libsamplerate-js, dependencies, @alexanderolsen/libsamplerate-js, @dannadori/voice-changer-client-js, @dannadori/voice-changer-js, @dannadori/worker-manager, @fortawesome/fontawesome-svg-core, @fortawesome/free-brands-svg-icons (+41 more)

### Community 25 - "diffusion_svc_model/nsf_hifigan/models.py"
Cohesion: 0.06
Nodes (15): DiscriminatorP, DiscriminatorS, Generator, MultiPeriodDiscriminator, MultiScaleDiscriminator, no_grad, Definition of sine generator SineGen(samp_rate, harmonic_num = 0, sine_amp =…, sine_tensor, uv = forward(f0) input F0: tensor(batchsize=1, length, dim=1) f0… (+7 more)

### Community 26 - "p"
Cohesion: 0.08
Nodes (5): chooseRemoteVideoSources(), getVideoTileArea(), p, updateIndex(), wantsResubscribe()

### Community 27 - "D"
Cohesion: 0.09
Nodes (4): D, pe(), protocols(), url()

### Community 28 - "infer_pack/modules.py"
Cohesion: 0.07
Nodes (17): fused_add_tanh_sigmoid_multiply(), ConvFlow, ConvReluNorm, DDSConv, ElementwiseAffine, Flip, LayerNorm, Log (+9 more)

### Community 29 - ".updateRemoteVideosFromLastVideosToReceive"
Cohesion: 0.07
Nodes (14): debugDumpTransceivers(), getMidForStreamId(), groupIdForStreamId(), overrideStreamIdMappings(), setStreamIdForMid(), setupLocalTransceivers(), StreamIdsInSameGroup(), subscribeFrameSent() (+6 more)

### Community 30 - "useAppState"
Cohesion: 0.10
Nodes (28): useAppState(), addToCatalog(), catalog, initialize(), HeaderArea(), HeaderAreaProps, ModelSlotArea(), ModelSlotAreaProps (+20 more)

### Community 31 - "SiFiGANGenerator"
Cohesion: 0.08
Nodes (24): Calculate forward propagation. Args: x (Tensor): Input sine signal (B, 1, T). c…, SiFiGAN generator module., Reset parameters. This initialization follows the official implementation…, Remove weight normalization module from all of the layers., Apply weight normalization module from all of the layers., Initialize SiFiGANGenerator module. Args: in_channels (int): Number of input…, SiFiGANGenerator, AdaptiveResidualBlock (+16 more)

### Community 32 - "ddsp/pcmer.py"
Cohesion: 0.09
Nodes (18): calc_same_padding(), ConformerConvModule, default(), DepthWiseConv1d, empty(), _EncoderLayer, exists(), FastAttention (+10 more)

### Community 33 - "naive/pcmer.py"
Cohesion: 0.09
Nodes (18): calc_same_padding(), ConformerConvModule, default(), DepthWiseConv1d, empty(), _EncoderLayer, exists(), FastAttention (+10 more)

### Community 34 - "MMVCv13/models/models.py"
Cohesion: 0.10
Nodes (14): fused_add_tanh_sigmoid_multiply(), get_padding(), init_weights(), sequence_mask(), Generator, PosteriorEncoder, Synthesizer for Training, ResidualCouplingBlock (+6 more)

### Community 35 - "hubert/model.py"
Cohesion: 0.10
Nodes (20): inference_mode, LongTensor, _compute_mask(), FeatureExtractor, FeatureProjection, Hubert, hubert_discrete(), hubert_soft() (+12 more)

### Community 36 - "devDependencies"
Cohesion: 0.05
Nodes (37): eslint, eslint-config-prettier, eslint-plugin-prettier, eslint-plugin-react, @types/node, typescript, webpack, devDependencies (+29 more)

### Community 37 - "DPM_Solver"
Cohesion: 0.09
Nodes (19): DPM_Solver, Construct a DPM-Solver. We support both DPM-Solver…, Return the noise prediction model., Return the data prediction model (with corrector)., Convert the model to the noise prediction model or the data prediction model., Compute the intermediate time steps for sampling. Args: skip_type: A `str`. The…, Get the order of each step for sampling by the singlestep DPM-Solver. We…, Denoise at the final step, which is equivalent to solve the ODE from lambda_s… (+11 more)

### Community 38 - "VoiceChangerModel"
Cohesion: 0.07
Nodes (9): BeatriceModelSlot, Beatrice, AudioInOut, Any, AudioInOut, VoiceChangerIF, Any, AudioInOut (+1 more)

### Community 40 - "tools.py"
Cohesion: 0.08
Nodes (14): Audio2ContentVec, Audio2ContentVec768, Audio2ContentVec768L12, Audio2HubertBase, Audio2HubertBase768, Audio2HubertBase768L12, Audio2HubertLarge1024L24, Audio2HubertSoft (+6 more)

### Community 41 - "whisper/model.py"
Cohesion: 0.10
Nodes (15): AudioEncoder, LayerNorm, Linear, ModelDimensions, MultiHeadAttention, Tensor, x : torch.Tensor, shape = (batch_size, n_mels, n_ctx) the mel spectrogram of…, x : torch.LongTensor, shape = (batch_size, <= n_ctx) the text tokens xa :… (+7 more)

### Community 42 - "MultiHeadAttention"
Cohesion: 0.10
Nodes (15): Decoder, Encoder, FFN, FFT, MultiHeadAttention, x: [b, h, l, m] y: [h or 1, m, d] ret: [b, h, l, d], x: [b, h, l, d] y: [h or 1, m, d] ret: [b, h, l, m], x: [b, h, l, 2*l-1] ret: [b, h, l, l] (+7 more)

### Community 43 - "lib/src/const.ts"
Cohesion: 0.06
Nodes (33): BeatriceModelSlot, CrossFadeOverlapSize, DDSPSVCModelSlot, DiffMethod, DiffusionSVCModelSlot, DiffusionSVCSampleModel, F0Detector, INDEXEDDB_DB_APP_NAME (+25 more)

### Community 44 - "diffusion_onnx.py"
Cohesion: 0.12
Nodes (15): cosine_beta_schedule(), default(), exists(), extract(), GaussianDiffusion, noise_like(), predict_stage0(), predict_stage1() (+7 more)

### Community 45 - "001_GuiStateProvider.tsx"
Cohesion: 0.07
Nodes (29): AnimationTypes, HeaderButtonProps, GuiStateAndMethod, GuiStateContext, GuiStateProvider(), OpenAdvancedSettingCheckbox, OpenAdvancedSettingDialogCheckbox, OpenConverterSettingCheckbox (+21 more)

### Community 46 - "useClient.ts"
Cohesion: 0.11
Nodes (26): InternalCallback, VoiceChangerWorkletListener, ClientSetting, DefaultClientSettng, DownSamplingMode, VOICE_CHANGER_CLIENT_EXCEPTION, VoiceChangerClientSetting, WorkletNodeSetting (+18 more)

### Community 47 - "Embedder"
Cohesion: 0.10
Nodes (15): Embedder, device, EmbedderType, device, EmbedderType, FairseqContentvec, device, FairseqHubert (+7 more)

### Community 48 - "SoVitsSvc40.py"
Cohesion: 0.10
Nodes (17): get_cluster_center_result(), get_cluster_model(), get_cluster_result(), x: np.array [t, 256] return cluster class result, get_hparams_from_file(), get_hubert_content(), interpolate_f0(), load_checkpoint() (+9 more)

### Community 49 - "SoVitsSvc40/models/models.py"
Cohesion: 0.10
Nodes (14): DiscriminatorP, DiscriminatorS, Encoder, F0Decoder, MultiPeriodDiscriminator, Synthesizer for Training, ResidualCouplingBlock, SynthesizerTrn (+6 more)

### Community 50 - "modules/modules.py"
Cohesion: 0.08
Nodes (12): fused_add_tanh_sigmoid_multiply(), init_weights(), _script_if_tracing, ConvReluNorm, DDSConv, ElementwiseAffine, Log, Dialted and Depth-Separable Convolution (+4 more)

### Community 51 - "join"
Cohesion: 0.11
Nodes (21): allStreams(), allVideoSendingSourcesExcludingSelf(), buildAttendeeToSortedStreamDescriptorMapExcludingSelf(), calculateOptimalReceiveSet(), chooseEncodingParameters(), get(), getDateString(), getDateTimeString() (+13 more)

### Community 52 - "AppSettingProvider.tsx"
Cohesion: 0.11
Nodes (25): ApplicationSetting, CorpusTextSetting, fetchApplicationSetting(), InitialApplicationSetting, StorageTypes, ApplicationSettingManagerStateAndMethod, useApplicationSettingManager(), IndexedDBState (+17 more)

### Community 53 - "DPM_Solver"
Cohesion: 0.11
Nodes (16): DPM_Solver, Compute the noised input xt = alpha_t * x + sigma_t * noise. Args: x: A…, Inverse the sample `x` from time `t_start` to `t_end` by DPM-Solver. For…, Compute the sample at time `t_end` by DPM-Solver, given the initial `x` at time…, Construct a DPM-Solver. We support both DPM-Solver…, Return the noise prediction model., Return the data prediction model (with corrector)., Convert the model to the noise prediction model or the data prediction model. (+8 more)

### Community 54 - ".__init__"
Cohesion: 0.09
Nodes (10): BiGRU, ConvBlockRes, Decoder, DeepUnet, E2E, Encoder, Intermediate, MelSpectrogram (+2 more)

### Community 55 - "MMVCv15/models/models.py"
Cohesion: 0.13
Nodes (11): fused_add_tanh_sigmoid_multiply(), get_padding(), init_weights(), sequence_mask(), Generator, ResidualCouplingBlock, Flip, ResBlock1 (+3 more)

### Community 56 - "models/utils.py"
Cohesion: 0.07
Nodes (9): clean_checkpoints(), compute_f0_dio(), deprecated(), get_hparams(), get_hparams_from_dir(), HParams, Freeing up space by deleting saved ckpts Arguments: path_to_models -- Path to…, This is a decorator which can be used to mark functions as deprecated. It will… (+1 more)

### Community 57 - "AppStateProvider.tsx"
Cohesion: 0.11
Nodes (20): fetchTextResource(), CorpusDataState, CorpusDataStateAndMethod, CorpusTextData, useCorpusData(), AudioStreamer, MediaRecorderState, MediaRecorderStateAndMethod (+12 more)

### Community 58 - "useMessageBuilder"
Cohesion: 0.15
Nodes (20): WaitingDialog(), MainScreen(), MainScreenProps, SampleDownloaderScreen(), SampleDownloaderScreenProps, FileUploaderScreen(), FileUploaderScreenProps, EditorScreen() (+12 more)

### Community 59 - "useAppSetting"
Cohesion: 0.14
Nodes (17): useAppSetting(), Header(), DeviceManagerProps, DeviceSelector(), DeviceType, Body(), CorpusSelector(), TextIndexSelector() (+9 more)

### Community 60 - "load_model_vocoder_from_combo"
Cohesion: 0.11
Nodes (14): l2_regularization(), input: B x n_frames x n_unit return: dict of B x n_frames x feat, Unit2MelNaive, PCmer, The encoder that is used in the Transformer model., DotDict, load_model_vocoder(), load_model_vocoder_from_combo() (+6 more)

### Community 61 - ".__init__"
Cohesion: 0.10
Nodes (12): Conv1d, get_padding(), init_weights(), DiscriminatorP, DiscriminatorS, MultiPeriodDiscriminator, MultiPeriodDiscriminatorV2, Definition of sine generator SineGen(samp_rate, harmonic_num = 0, sine_amp =… (+4 more)

### Community 62 - "DiffusionSVC"
Cohesion: 0.11
Nodes (8): loadAllSlotInfo(), DiffusionSVC, AudioInOut, DiffusionSVCModelSlot, DiffusionSVCSettings, ModelSlotManager, ModelSlots, StaticSlot

### Community 63 - "MultiHeadAttention"
Cohesion: 0.12
Nodes (11): Decoder, FFN, MultiHeadAttention, x: decoder input h: encoder output, x: [b, h, l, m] y: [h or 1, m, d] ret: [b, h, l, d], x: [b, h, l, 2*l-1] ret: [b, h, l, l], x: [b, h, l, l] ret: [b, h, l, 2*l-1], Bias for self-attention to encourage attention to close positions. Args:… (+3 more)

### Community 64 - "t"
Cohesion: 0.12
Nodes (3): t(), s(), t()

### Community 65 - "UniPC"
Cohesion: 0.12
Nodes (14): expand_dims(), model_wrapper(), Create a wrapper function for the noise prediction model., Construct a UniPC. We support both data_prediction and noise_prediction., The dynamic thresholding method., Return the noise prediction model., Return the data prediction model (with corrector)., Convert the model to the noise prediction model or the data prediction model. (+6 more)

### Community 66 - "Conv2d"
Cohesion: 0.10
Nodes (9): Conv2d, Conv2d module with customized initialization., Initialize Conv2d module., IMDCT, LayerNorm, LoRALinear1d, LoRALinear2d, MBConv2d (+1 more)

### Community 67 - "package.json"
Cohesion: 0.08
Nodes (25): keywords, keywords, author, bugs, url, description, homepage, voice conversion (+17 more)

### Community 68 - "207-1MelSpectrogramUtil.ts"
Cohesion: 0.15
Nodes (24): applyFilterbank(), applyWholeFilterbank(), applyWindow(), calculateFftFreqs(), calculateMelFreqs(), createMelFilterbank(), fft(), frame() (+16 more)

### Community 69 - "scripts"
Cohesion: 0.08
Nodes (24): author, description, license, main, name, scripts, build:dev, build:mod (+16 more)

### Community 70 - ".of"
Cohesion: 0.11
Nodes (8): audioVideoDidStop(), forEachContentShareObserver(), haveVideoTilesWithStreams(), healthIfChanged(), pauseContentShare(), ping(), setupContentShareEvents(), unpauseContentShare()

### Community 71 - "GaussianDiffusion"
Cohesion: 0.15
Nodes (10): cosine_beta_schedule(), default(), exists(), extract(), GaussianDiffusion, noise_like(), no_grad, Use the PLMS method from [Pseudo Numerical Methods for Diffusion Models on… (+2 more)

### Community 72 - "ServerDevice"
Cohesion: 0.16
Nodes (8): checkSamplingRate(), dummy_callback(), list_audio_device(), ndarray, ServerAudioDevice, ndarray, ServerDevice, ServerAudioDeviceType

### Community 73 - "useAppRoot"
Cohesion: 0.12
Nodes (12): App(), AppStateWrapper(), root, useAppRoot(), AppStateProvider(), ErrorBoundary, ErrorBoundaryProps, ErrorBoundaryState (+4 more)

### Community 74 - "ddsp/vocoder.py"
Cohesion: 0.14
Nodes (13): PCmer, The encoder that is used in the Transformer model., Split a tensor into a dictionary of multiple tensors., input: B x n_frames x n_unit return: dict of B x n_frames x feat, split_to_dict(), Unit2Control, Audio2HubertSoft, CombSub (+5 more)

### Community 75 - ".__init__"
Cohesion: 0.08
Nodes (8): Audio2ContentVec, Audio2ContentVec768, Audio2ContentVec768L12, Audio2HubertBase, Audio2HubertBase768, Audio2HubertBase768L12, Audio2HubertLarge1024L24, CNHubertSoftFish

### Community 76 - "infer_pack/commons.py"
Cohesion: 0.11
Nodes (12): SynthesizerTrnMsNSFsidNono, add_timing_signal_1d(), cat_timing_signal_1d(), generate_path(), get_timing_signal_1d(), rand_gumbel(), rand_gumbel_like(), rand_slice_segments() (+4 more)

### Community 77 - "dependencies"
Cohesion: 0.09
Nodes (23): protobufjs, react-dom, dependencies, amazon-chime-sdk-js, buffer, localforage, protobufjs, react (+15 more)

### Community 78 - "HParams"
Cohesion: 0.12
Nodes (9): convert_continuos_f0(), get_hparams_from_file(), HParams, load_checkpoint(), Zero-pads model inputs and targets, spectrogram_torch(), TextAudioSpeakerCollate, convert() (+1 more)

### Community 79 - "GaussianDiffusion"
Cohesion: 0.17
Nodes (9): cosine_beta_schedule(), default(), exists(), extract(), GaussianDiffusion, noise_like(), no_grad, conditioning diffusion, use fastspeech2 encoder output as the condition (+1 more)

### Community 80 - "NoiseScheduleVP"
Cohesion: 0.11
Nodes (14): expand_dims(), interpolate_fn(), model_wrapper(), NoiseScheduleVP, Create a wrapper function for the noise prediction model. DPM-Solver needs to…, A piecewise linear function y = f(x), using xp and yp as keypoints. We…, Expand the tensor `v` to the dim `dims`. Args: `v`: a PyTorch tensor with shape…, The dynamic thresholding method. (+6 more)

### Community 81 - "NsfHifiGAN"
Cohesion: 0.13
Nodes (7): NsfHifiGAN, NsfHifiGANLog10, load_config(), load_model(), dynamic_range_compression_torch(), load_wav_to_torch(), STFT

### Community 82 - "voras_beta/commons.py"
Cohesion: 0.12
Nodes (17): add_timing_signal_1d(), cat_timing_signal_1d(), convert_pad_shape(), fused_add_tanh_sigmoid_multiply(), generate_path(), get_padding(), get_timing_signal_1d(), init_weights() (+9 more)

### Community 83 - "CrepePitchExtractor"
Cohesion: 0.11
Nodes (13): BasePitchExtractor, CrepePitchExtractor, MaskedAvgPool1d, MaskedMedianPool1d, ndarray, Tensor, An implementation of mean pooling that supports masked values. Args:…, Repeat content to target length. This is a wrapper of… (+5 more)

### Community 84 - "useGuiState"
Cohesion: 0.22
Nodes (12): useGuiState(), StartingNoticeDialog(), ModelSlotManagerDialog(), MergeLabDialog(), AdvancedSettingDialog(), GetServerInfomationDialog(), GetClientInfomationDialog(), EnablePassThroughDialog() (+4 more)

### Community 85 - "scripts"
Cohesion: 0.09
Nodes (21): author, description, directories, lib, license, main, name, scripts (+13 more)

### Community 86 - "ddsp/core.py"
Cohesion: 0.15
Nodes (16): apply_dynamic_window_to_impulse_response(), apply_window_to_impulse_response(), crop_and_compensate_delay(), fft_convolve(), frequency_filter(), frequency_impulse_response(), get_fft_size(), MaskedAvgPool1d() (+8 more)

### Community 87 - "models/diffusion/unit2mel.py"
Cohesion: 0.14
Nodes (9): DotDict, load_model_vocoder(), dict, input: B x n_frames x n_unit return: dict of B x n_frames x feat, Unit2Mel, :param spec: [B, 1, M, T] :param diffusion_step: [B, 1] :param cond: [B, M, T]…, ResidualBlock, SinusoidalPosEmb (+1 more)

### Community 88 - ".__init__"
Cohesion: 0.14
Nodes (7): Conv1d, DiscriminatorS, Generator, ResBlock1, ResBlock2, get_padding(), init_weights()

### Community 90 - "TorchCrepe2.py"
Cohesion: 0.14
Nodes (17): bins_to_cents(), cents_to_bins(), cents_to_frequency(), dither(), frequency_to_bins(), frequency_to_cents(), periodicity(), Converts pitch bins to cents (+9 more)

### Community 91 - "demo/src/const.ts"
Cohesion: 0.16
Nodes (16): DeviceArea(), DeviceAreaProps, downloadRecord(), RecorderArea(), RecorderAreaProps, AUDIO_ELEMENT_FOR_PLAY_MONITOR, AUDIO_ELEMENT_FOR_PLAY_RESULT, AUDIO_ELEMENT_FOR_SAMPLING_INPUT (+8 more)

### Community 92 - "useServerSetting.ts"
Cohesion: 0.13
Nodes (16): FileChunk, DefaultServerSetting, MergeModelRequest, OnnxExporterInfo, ServerInfo, ServerSettingKey, VoiceChangerServerSetting, VoiceChangerType (+8 more)

### Community 94 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowSyntheticDefaultImports, declaration, esModuleInterop, forceConsistentCasingInFileNames, moduleResolution, noImplicitAny, noImplicitReturns (+10 more)

### Community 95 - "SvcDDSP.py"
Cohesion: 0.13
Nodes (6): F0_Extractor, Units_Encoder, Volume_Extractor, Enhancer, NsfHifiGAN, device

### Community 96 - "001_AppStateProvider.tsx"
Cohesion: 0.13
Nodes (15): useVCClient(), UseVCClientProps, VCClientState, f0ModelUrl, ModelSampleRateStr, noF0ModelUrl, useWebInfo(), UseWebInfoProps (+7 more)

### Community 97 - "SynthesizerTrn"
Cohesion: 0.12
Nodes (7): Collate's training batch from normalized text, audio and speaker identities…, dilated_factor(), Validate length Args: xs (ndarray): numpy array of features ys (ndarray): numpy…, Pitch-dependent dilated factor Args: batch_f0 (ndarray): the f0 sequence (T) fs…, validate_length(), Synthesizer for Training, SynthesizerTrn

### Community 98 - ".removeObserver"
Cohesion: 0.25
Nodes (5): addContentShareObserver(), removeContentShareObserver(), startContentShare(), startContentShareFromScreenCapture(), stopContentShare()

### Community 100 - ".pause"
Cohesion: 0.15
Nodes (8): bindVideoElement(), captureVideoTile(), getVideoTile(), pauseVideoTile(), registerObserver(), sendTileStateUpdate(), unbindVideoElement(), unpauseVideoTile()

### Community 101 - "voras_beta/utils.py"
Cohesion: 0.16
Nodes (9): DatasetMetadata, DatasetMetaItem, BaseModel, TrainConfig, TrainConfigData, TrainConfigModel, TrainConfigTrain, load_audio() (+1 more)

### Community 102 - "SnakeFilter"
Cohesion: 0.12
Nodes (5): CausalConvTranspose1d, DilatedCausalConv1d, Adaptive filter using snakebeta, padding = 0, dilation = 1のとき Lout = (Lin - 1) * stride + kernel_rate * stride +…, SnakeFilter

### Community 103 - "compilerOptions"
Cohesion: 0.12
Nodes (17): compilerOptions, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib, moduleResolution (+9 more)

### Community 104 - "compilerOptions"
Cohesion: 0.12
Nodes (17): compilerOptions, allowSyntheticDefaultImports, declaration, esModuleInterop, forceConsistentCasingInFileNames, lib, moduleResolution, noImplicitAny (+9 more)

### Community 106 - "LLVC"
Cohesion: 0.13
Nodes (7): LLVCModelSlot, LLVC, LLVCSetting, Any, AudioInOut, AudioInOutFloat, データ前処理(torch independent) ・マルチディメンション処理 ・リサンプリング( 入力sr -> 16K) ・バターフィルタ Args:…

### Community 107 - "useAppState"
Cohesion: 0.26
Nodes (12): useAppState(), ExportController(), WaveSurferView(), powerToDb(), MelSpectrogram(), MelTypes, convert48KhzTo24Khz(), drawMel() (+4 more)

### Community 108 - "compilerOptions"
Cohesion: 0.12
Nodes (17): compilerOptions, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib, moduleResolution (+9 more)

### Community 109 - "NoiseScheduleVP"
Cohesion: 0.15
Nodes (10): interpolate_fn(), NoiseScheduleVP, For some beta schedules such as cosine schedule, the log-SNR has numerical…, A piecewise linear function y = f(x), using xp and yp as keypoints. We…, Compute log(alpha_t) of a given continuous-time label t in [0, T]., Compute alpha_t of a given continuous-time label t in [0, T]., Create a wrapper class for the forward SDE (VP type). *** Update: We support…, Compute sigma_t of a given continuous-time label t in [0, T]. (+2 more)

### Community 111 - "modules/commons.py"
Cohesion: 0.17
Nodes (13): add_timing_signal_1d(), cat_timing_signal_1d(), generate_path(), get_timing_signal_1d(), rand_gumbel(), rand_gumbel_like(), rand_slice_segments(), rand_slice_segments_with_pitch() (+5 more)

### Community 112 - "MockStream"
Cohesion: 0.12
Nodes (4): MockStream, MyCustomNamespace, load_wav_to_torch(), load_wav_to_torch()

### Community 113 - "recorder/package.json"
Cohesion: 0.12
Nodes (15): author, description, keywords, license, main, name, scripts, build (+7 more)

### Community 114 - "models/diffusion/vocoder.py"
Cohesion: 0.18
Nodes (5): NsfHifiGAN, NsfHifiGANLog10, Vocoder, load_config(), load_model()

### Community 115 - "models/nsf_hifigan/models.py"
Cohesion: 0.14
Nodes (5): AttrDict, dict, DiscriminatorP, MultiPeriodDiscriminator, MultiScaleDiscriminator

### Community 116 - ".__init__"
Cohesion: 0.15
Nodes (5): DiscriminatorP, DiscriminatorS, MultiPeriodDiscriminator, PosteriorEncoder, TextEncoder

### Community 117 - "001_AppRootProvider.tsx"
Cohesion: 0.19
Nodes (12): AppGuiSetting, AppGuiSettingState, AppGuiSettingStateAndMethod, GuiComponentSetting, InitialAppGuiDemoSetting, useAppGuiSetting(), AudioConfigState, useAudioConfig() (+4 more)

### Community 120 - "Ae"
Cohesion: 0.31
Nodes (3): Ae, Le(), Ve()

### Community 122 - "Resample"
Cohesion: 0.17
Nodes (7): Resample, F0_Extractor, masked_avg_pool_1d(), median_pool_1d(), no_grad, Units_Encoder, AudioInOut

### Community 123 - ".__init__"
Cohesion: 0.18
Nodes (5): AfterDiffusion, DiffNet, Pred, ResidualBlock, SinusoidalPosEmb

### Community 124 - "NoiseScheduleVP"
Cohesion: 0.17
Nodes (9): interpolate_fn(), NoiseScheduleVP, Compute log(alpha_t) of a given continuous-time label t in [0, T]., Compute alpha_t of a given continuous-time label t in [0, T]., Compute sigma_t of a given continuous-time label t in [0, T]., Compute lambda_t = log(alpha_t) - log(sigma_t) of a given continuous-time label…, Compute the continuous-time label t in [0, T] of a given half-logSNR lambda_t., Create a wrapper class for the forward SDE (VP type). *** Update: We support… (+1 more)

### Community 125 - "CachedConvNet"
Cohesion: 0.15
Nodes (7): CachedConvNet, CausalConvBlock, Initialize context buffer for each layer., Args: x: [B, in_channels, T] Input ctx: {[B, channels, self.buf_length[0]],…, 1D Causal convolution., Based on https://github.com/f90/Seq-U-Net/blob/master/sequnet_res.py, ResidualBlock

### Community 126 - "GeneratorVoras"
Cohesion: 0.15
Nodes (3): GeneratorVoras, HarmonicEmbedder, WaveBlock

### Community 127 - "convert.py"
Cohesion: 0.18
Nodes (14): bins_to_cents(), bins_to_frequency(), cents_to_bins(), cents_to_frequency(), dither(), frequency_to_bins(), frequency_to_cents(), Converts pitch bins to cents (+6 more)

### Community 129 - "VolumeExtractor"
Cohesion: 0.21
Nodes (5): Tensor, upsample(), VolumeExtractor, Inferencer, PitchExtractor

### Community 130 - "Conv1d"
Cohesion: 0.21
Nodes (5): Conv1d, :param spec: [B, 1, M, T] :param diffusion_step: [B, 1] :param cond: [B, M, T]…, ResidualBlock, SinusoidalPosEmb, WaveNet

### Community 131 - "DiffusionSVCInferencer"
Cohesion: 0.23
Nodes (6): DiffusionSVCInferencer, Inferencer, no_grad, Tensor, DiffusionSVCInferenceType, Inferencer

### Community 132 - "SignalGenerator"
Cohesion: 0.23
Nodes (8): no_grad, Calculate noise signals. Args: f0 (Tensor): F0 tensor (B, 1, T // hop_size).…, Calculate sine signals. Args: f0 (Tensor): F0 tensor (B, 1, T // hop_size).…, Calculate sines. Args: f0 (Tensor): F0 tensor (B, 1, T // hop_size). Returns:…, Calculate V/UV binary sequences. Args: f0 (Tensor): F0 tensor (B, 1, T //…, Input signal generator module., Initialize WaveNetResidualBlock module. Args: sample_rate (int): Sampling rate.…, SignalGenerator

### Community 133 - "IMDCTSymExpHead"
Cohesion: 0.16
Nodes (9): FourierHead, IMDCTSymExpHead, Tensor, Base class for inverse fourier modules., Args: x (Tensor): Input tensor of shape (B, L, H), where B is the batch size, L…, Apply the Inverse Modified Discrete Cosine Transform (IMDCT) to the input MDCT…, IMDCT Head module for predicting MDCT coefficients with symmetric exponential…, Forward pass of the IMDCTSymExpHead module. Args: x (Tensor): Input tensor of… (+1 more)

### Community 134 - "webpack_web.common.js"
Cohesion: 0.15
Nodes (10): CopyPlugin, HtmlWebpackPlugin, path, webpack, common, express, { merge }, path (+2 more)

### Community 135 - "100_useFrontendManager.ts"
Cohesion: 0.24
Nodes (9): FrontendManagerState, StateControls, useFrontendManager(), AnimationTypes, HeaderButton(), HeaderButtonProps, RightSidebarButton(), StateControlCheckbox (+1 more)

### Community 136 - "diffusion_svc_model/DiffusionSVC.py"
Cohesion: 0.21
Nodes (4): cross_fade(), GE2E, ndarray, SpeakerEncoder

### Community 137 - "filter.py"
Cohesion: 0.22
Nodes (12): mean(), median(), nanfilter(), nanmean(), nanmedian(), nanmedian1d(), Averave filtering for signals containing nan values Arguments signals…, Computes the median. If signal is empty, returns torch.nan Arguments signal… (+4 more)

### Community 138 - "threshold.py"
Cohesion: 0.15
Nodes (6): At, Hysteresis, Set periodicity to zero in silent regions, Simple thresholding at a specified probability value, Hysteresis thresholding, Silence

### Community 139 - "Generator"
Cohesion: 0.18
Nodes (4): Generator, ResBlock1, ResBlock2, init_weights()

### Community 140 - "102_ConfigArea.tsx"
Cohesion: 0.21
Nodes (8): QualityArea(), QualityAreaProps, ConvertArea(), ConvertProps, MoreActionArea(), MoreActionAreaProps, ConfigArea(), ConfigAreaProps

### Community 141 - "demo/webpack.common.js"
Cohesion: 0.17
Nodes (9): CopyPlugin, HtmlWebpackPlugin, path, webpack, common, { merge }, path, common (+1 more)

### Community 142 - "VoiceChangerWorkletProcessor"
Cohesion: 0.21
Nodes (5): RequestType, ResponseType, VoiceChangerWorkletProcessor, VoiceChangerWorkletProcessorRequest, VoiceChangerWorkletProcessorResponse

### Community 143 - "recorder/webpack.common.js"
Cohesion: 0.17
Nodes (9): CopyPlugin, HtmlWebpackPlugin, path, webpack, common, { merge }, path, common (+1 more)

### Community 144 - "Unit2Mel"
Cohesion: 0.26
Nodes (5): DotDict, load_model_vocoder(), dict, input: B x n_frames x n_unit return: dict of B x n_frames x feat, Unit2Mel

### Community 146 - "log_mel_spectrogram"
Cohesion: 0.20
Nodes (9): log_mel_spectrogram(), mel_filters(), pad_or_trim(), ndarray, Tensor, Pad or trim the audio array to N_SAMPLES, as expected by the encoder., load the mel filterbank matrix for projecting STFT into a Mel spectrogram.…, Compute the log-Mel spectrogram of Parameters ---------- audio: Union[str,… (+1 more)

### Community 147 - "onnxcrepe/core.py"
Cohesion: 0.23
Nodes (10): infer(), periodicity(), postprocess(), predict(), preprocess(), Convert audio to model input Arguments audio (numpy.ndarray [shape=(time,)])…, Forward pass through the model Arguments session…, Convert model output to F0 and periodicity Arguments probabilities… (+2 more)

### Community 152 - "ci"
Cohesion: 0.25
Nodes (10): ca(), ci, da(), fa(), la(), lr(), nr(), oa() (+2 more)

### Community 153 - "STFT"
Cohesion: 0.24
Nodes (3): dynamic_range_compression_torch(), load_wav_to_torch(), STFT

### Community 154 - "SineGen"
Cohesion: 0.18
Nodes (6): no_grad, Definition of sine generator SineGen(samp_rate, harmonic_num = 0, sine_amp =…, sine_tensor, uv = forward(f0) input F0: tensor(batchsize=1, length, dim=1) f0…, SourceModule for hn-nsf SourceModule(sampling_rate, harmonic_num=0,…, SineGen, SourceModuleHnNSF

### Community 155 - "llvc.py"
Cohesion: 0.20
Nodes (6): DilatedCausalConvEncoder, MaskNet, A dilated causal convolution based encoder for encoding time domain audio input…, Returns an initialized context buffer for a given batch size., Encodes input audio `x` into latent space, and aggregates contextual…, Generates a mask based on encoded input `e` and the one-hot label `label`.…

### Community 156 - "decode.py"
Cohesion: 0.24
Nodes (10): _apply_weights(), argmax(), ndarray, Sample observations by taking the argmax, Sample observations using weighted sum near the argmax, Sample observations using viterbi decoding, Sample observations combining viterbi decoding and weighted argmax, viterbi() (+2 more)

### Community 158 - "vdecoder/nsf_hifigan/nvSTFT.py"
Cohesion: 0.24
Nodes (3): dynamic_range_compression_torch(), load_wav_to_torch(), STFT

### Community 159 - "vdecoder/nsf_hifigan/models.py"
Cohesion: 0.22
Nodes (3): DiscriminatorP, MultiPeriodDiscriminator, get_padding()

### Community 160 - "SineGen"
Cohesion: 0.20
Nodes (6): no_grad, sine_tensor, uv = forward(f0) input F0: tensor(batchsize=1, length, dim=1) f0…, SourceModule for hn-nsf SourceModule(sampling_rate, harmonic_num=0,…, Definition of sine generator SineGen(samp_rate, harmonic_num = 0, sine_amp =…, SineGen, SourceModuleHnNSF

### Community 161 - "node_modules"
Cohesion: 0.22
Nodes (8): exclude, include, src/**/*.ts, exclude, include, node_modules, src/**/*.ts, src/**/*.tsx

### Community 162 - "webpack.worklet.dev.js"
Cohesion: 0.20
Nodes (7): path, common, { merge }, worklet, common, { merge }, worklet

### Community 164 - "002_useDeviceManager.ts"
Cohesion: 0.27
Nodes (6): DeviceInfo, DeviceManager, UpdateListener, DeviceManagerState, DeviceManagerStateAndMethod, useDeviceManager()

### Community 165 - "DiffusionSVC_ONNX"
Cohesion: 0.33
Nodes (3): DiffusionSVC_ONNX, no_grad, Tensor

### Community 166 - "Net"
Cohesion: 0.27
Nodes (5): LLVCInferencer, AudioInOutFloat, Tensor, Net, Extracts the audio corresponding to the `label` in the given `mixture`.…

### Community 167 - "PositionalEncoding"
Cohesion: 0.20
Nodes (6): CausalTransformerDecoderLayer, PositionalEncoding, Tensor, This class implements the absolute sinusoidal positional encoding function.…, Adapted from: "https://github.com/alexmt-scale/causal-transformer-…, Arguments --------- x : tensor Input feature shape (batch, time, fea)

### Community 168 - ".__init__"
Cohesion: 0.24
Nodes (4): DepthwiseSeparableConv, LayerNormPermuted, Args: x: [B, C, T], Depthwise separable convolutions

### Community 169 - "voras_beta/models.py"
Cohesion: 0.29
Nodes (4): DiscriminatorP, MultiPeriodDiscriminator, ConvNext2d, Causal ConvNext Block stride = 1 only

### Community 170 - "mel_processing.py"
Cohesion: 0.29
Nodes (8): dynamic_range_compression_torch(), dynamic_range_decompression_torch(), mel_spectrogram_torch(), PARAMS ------ C: compression factor used to compress, PARAMS ------ C: compression factor, spec_to_mel_torch(), spectral_de_normalize_torch(), spectral_normalize_torch()

### Community 171 - "hifigan/nvSTFT.py"
Cohesion: 0.27
Nodes (3): dynamic_range_compression_torch(), load_wav_to_torch(), STFT

### Community 173 - "index.ts"
Cohesion: 0.25
Nodes (4): ModelLoadException, fileSelector(), fileSelectorAsDataURL(), validateUrl()

### Community 175 - "lib/webpack.common.js"
Cohesion: 0.22
Nodes (6): path, webpack, common, { merge }, common, { merge }

### Community 176 - "AudioDataset"
Cohesion: 0.31
Nodes (4): Dataset, AudioDataset, get_data_loaders(), traverse_dir()

### Community 178 - "SSSLoss"
Cohesion: 0.28
Nodes (4): Single-scale Spectral Loss., Random-scale Spectral Loss., RSSLoss, SSSLoss

### Community 179 - "ServerDeviceCallbacks"
Cohesion: 0.22
Nodes (3): AudioInOut, ServerDeviceCallbacks, ServerDeviceSettings

### Community 180 - "WebUIInferencer"
Cohesion: 0.28
Nodes (4): SynthesizerTrnMsNSFsid, Inferencer, Tensor, WebUIInferencer

### Community 182 - "AWP"
Cohesion: 0.28
Nodes (3): AWP, Fast AWP https://www.kaggle.com/code/junkoda/fast-awp, Restore model parameter to correct position; AWP do not perturbe weights, it…

### Community 183 - "modules/enhancer.py"
Cohesion: 0.28
Nodes (3): Enhancer, NsfHifiGAN, load_model()

### Community 185 - "onnxcrepe/__init__.py"
Cohesion: 0.29
Nodes (3): no_grad, audio(), CrepeInferenceSession

### Community 186 - "Slicer"
Cohesion: 0.32
Nodes (3): cut(), Slicer, split()

### Community 187 - "CausalTransformerDecoder"
Cohesion: 0.29
Nodes (5): CausalTransformerDecoder, mod_pad(), A casual transformer decoder which decodes input vectors using precisely…, Unfolds the sequence into a batch of sequences prepended with `ctx_len`…, Args: x: [B, model_dim, T] ctx_buf: [B, num_layers, model_dim, ctx_len]

### Community 188 - "index_initial"
Cohesion: 0.29
Nodes (5): index_initial(), pd_indexing(), Pitch-dependent indexing of past and future samples. Args: x (Tensor): Input…, Tensor batch and channel index initialization. Args: n_batch (Int): Number of…, Calculate forward propagation. Args: x (Tensor): Input tensor (B, channels, T).…

### Community 190 - "diffusion_svc_model/diffusion/dpm_solver_pytorch.py"
Cohesion: 0.29
Nodes (5): expand_dims(), model_wrapper(), Expand the tensor `v` to the dim `dims`. Args: `v`: a PyTorch tensor with shape…, Create a wrapper function for the noise prediction model. DPM-Solver needs to…, The dynamic thresholding method.

### Community 191 - "EmbedderProtocol"
Cohesion: 0.29
Nodes (3): EmbedderProtocol, device, Tensor

### Community 193 - "npm-run-all"
Cohesion: 0.33
Nodes (6): npm-run-all, npm-run-all, devDependencies, npm-run-all, npm-run-all, npm-run-all

### Community 197 - ".multistep_dpm_solver_update"
Cohesion: 0.33
Nodes (3): Multistep solver DPM-Solver-2 from time `t_prev_list[-1]` to time `t`. Args: x:…, Multistep solver DPM-Solver-3 from time `t_prev_list[-1]` to time `t`. Args: x:…, Multistep DPM-Solver with the order `order` from time `t_prev_list[-1]` to time…

### Community 201 - "voice-changer-worklet-processor.d.ts"
Cohesion: 0.40
Nodes (4): RequestType, ResponseType, VoiceChangerWorkletProcessorRequest, VoiceChangerWorkletProcessorResponse

### Community 204 - "Whisper"
Cohesion: 0.40
Nodes (3): device, Whisper, Tensor

### Community 205 - "voras_beta/transforms.py"
Cohesion: 0.80
Nodes (4): piecewise_rational_quadratic_transform(), rational_quadratic_spline(), searchsorted(), unconstrained_rational_quadratic_spline()

### Community 206 - ".__init__"
Cohesion: 0.40
Nodes (3): Any, Inferencer, PitchExtractor

### Community 207 - "loudness.py"
Cohesion: 0.50
Nodes (4): a_weighted(), perceptual_weights(), Retrieve the per-frame loudness, A-weighted frequency-dependent perceptual loudness weights

### Community 210 - "ts-loader"
Cohesion: 0.50
Nodes (4): ts-loader, ts-loader, ts-loader, ts-loader

### Community 211 - "@types/react-dom"
Cohesion: 0.50
Nodes (4): @types/react-dom, @types/react-dom, @types/react-dom, @types/react-dom

### Community 212 - "webpack-cli"
Cohesion: 0.50
Nodes (4): webpack-cli, webpack-cli, webpack-cli, webpack-cli

### Community 214 - "tsconfig.worklet.json"
Cohesion: 0.50
Nodes (3): exclude, include, worklet/src/*.ts

## Knowledge Gaps
- **391 isolated node(s):** `MelTypes`, `AppGuiSetting`, `AppGuiSettingState`, `GuiComponentSetting`, `AppRootValue` (+386 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1792 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `VoiceChangerParams` connect `VoiceChangerParams` to `DeviceManager`, `VoiceChangerManager`, `VoiceChangerModel`, `Timer2`, `LLVC`, `log_control.py`, `Embedder`, `EasyVC`, `SoVitsSvc40.py`, `RVCr2`, `VoiceChangerManager.py`, `RVC`, `DiffusionSVC`, `SvcDDSP.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `Protocol` connect `DeviceManager` to `VoiceChangerManager`, `VoiceChangerModel`, `EnumInferenceTypes`, `lib/src/const.ts`, `ServerDeviceCallbacks`, `VoiceChangerManager.py`, `EmbedderProtocol`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `DeviceManager` connect `DeviceManager` to `DiffusionSVC_ONNX`, `VoiceChangerParams`, `EnumInferenceTypes`, `log_control.py`, `WebUIInferencer`, `VoiceChangerManager.py`, `load_model_vocoder_from_combo`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 31 inferred relationships involving `i()` (e.g. with `a()` and `an()`) actually correct?**
  _`i()` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `s()` (e.g. with `d()` and `r()`) actually correct?**
  _`s()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `c()` (e.g. with `a()` and `i()`) actually correct?**
  _`c()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `n()` (e.g. with `a()` and `n()`) actually correct?**
  _`n()` has 4 INFERRED edges - model-reasoned connections that need verification._