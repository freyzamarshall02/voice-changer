import { ClampedNumberInput } from "../../ClampedNumberInput";
import React, { useMemo } from "react";
import { useAppState } from "../../../001_provider/001_AppStateProvider";

export type IndexAreaProps = {};

export const IndexArea = (_props: IndexAreaProps) => {
    const { serverSetting } = useAppState();

    const selected = useMemo(() => {
        if (serverSetting.serverSetting.modelSlotIndex == undefined) {
            return;
        } else {
            return serverSetting.serverSetting.modelSlots[serverSetting.serverSetting.modelSlotIndex];
        }
    }, [serverSetting.serverSetting.modelSlotIndex, serverSetting.serverSetting.modelSlots]);

    const indexArea = useMemo(() => {
        if (!selected) {
            return <></>;
        }
        if (selected.voiceChangerType != "RVC") {
            return <></>;
        }

        const currentIndexRatio = serverSetting.serverSetting.indexRatio;
        const indexRatioValueUpdatedAction = async (val: number) => {
            await serverSetting.updateServerSettings({ ...serverSetting.serverSetting, indexRatio: val });
        };

        const clampIndex = (val: number) => Math.min(1, Math.max(0, Math.round(val * 10) / 10));

        return (
            <div className="character-area-control">
                <div className="character-area-control-title">INDEX:</div>
                <div className="character-area-control-field">
                    <div className="character-area-slider-control">
                        <span className="character-area-slider-control-kind"></span>
                        <span className="character-area-slider-control-slider">
                            <input
                                type="range"
                                min="0"
                                max="1"
                                step="0.1"
                                value={currentIndexRatio}
                                onChange={(e) => {
                                    indexRatioValueUpdatedAction(Number(e.target.value));
                                }}
                            ></input>
                        </span>
                        <ClampedNumberInput
                            min={0}
                            max={1}
                            step={0.1}
                            value={currentIndexRatio}
                            style={{ width: "4em" }}
                            onChange={indexRatioValueUpdatedAction}
                        />
                        <span
                            style={{ cursor: "pointer", marginLeft: "4px", fontSize: "0.8em", padding: "1px 4px", border: "1px solid #888", borderRadius: "3px" }}
                            title="Reset to 0"
                            onClick={() => indexRatioValueUpdatedAction(0)}
                        >↺</span>
                    </div>
                </div>
            </div>
        );
    }, [serverSetting.serverSetting, serverSetting.updateServerSettings, selected]);

    return indexArea;
};
