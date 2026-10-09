import React, { useMemo } from "react";
import { useAppState } from "../../../001_provider/001_AppStateProvider";

export type TuningAreaProps = {};

export const TuningArea = (_props: TuningAreaProps) => {
    const { serverSetting, webInfoState, webEdition } = useAppState();

    const selected = useMemo(() => {
        if (webEdition) {
            return webInfoState.webModelslot;
        }
        if (serverSetting.serverSetting.modelSlotIndex == undefined) {
            return;
        } else {
            return serverSetting.serverSetting.modelSlots[serverSetting.serverSetting.modelSlotIndex];
        }
    }, [serverSetting.serverSetting.modelSlotIndex, serverSetting.serverSetting.modelSlots, webEdition]);

    const tuningArea = useMemo(() => {
        if (!selected) {
            return <></>;
        }

        let currentTuning;
        if (webEdition) {
            currentTuning = webInfoState.upkey;
        } else {
            currentTuning = serverSetting.serverSetting.tran;
        }
        const tranValueUpdatedAction = async (val: number) => {
            if (webEdition) {
                webInfoState.setUpkey(val);
            } else {
                await serverSetting.updateServerSettings({ ...serverSetting.serverSetting, tran: val });
            }
        };

        const clampTune = (val: number) => Math.min(50, Math.max(-50, Math.round(val)));

        return (
            <div className="character-area-control">
                <div className="character-area-control-title">TUNE:</div>
                <div className="character-area-control-field">
                    <div className="character-area-slider-control">
                        <span className="character-area-slider-control-kind"></span>
                        <span className="character-area-slider-control-slider">
                            <input
                                type="range"
                                min="-50"
                                max="50"
                                step="1"
                                value={currentTuning}
                                onChange={(e) => {
                                    tranValueUpdatedAction(Number(e.target.value));
                                }}
                            ></input>
                        </span>
                        <input
                            type="number"
                            min="-50"
                            max="50"
                            step="1"
                            value={currentTuning}
                            style={{ width: "4em" }}
                            onChange={(e) => {
                                tranValueUpdatedAction(clampTune(Number(e.target.value)));
                            }}
                        />
                        <span
                            style={{ cursor: "pointer", marginLeft: "4px", fontSize: "0.8em", padding: "1px 4px", border: "1px solid #888", borderRadius: "3px" }}
                            title="Reset to 0"
                            onClick={() => tranValueUpdatedAction(0)}
                        >↺</span>
                    </div>
                </div>
            </div>
        );
    }, [serverSetting.serverSetting, serverSetting.updateServerSettings, selected, webEdition, webInfoState.upkey]);

    return tuningArea;
};

