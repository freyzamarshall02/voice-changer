import React, { useState, useEffect } from "react";

export type ClampedNumberInputProps = {
    min: number;
    max: number;
    step: number;
    value: number;
    onChange: (val: number) => void;
    style?: React.CSSProperties;
};

export const ClampedNumberInput = ({ min, max, step, value, onChange, style }: ClampedNumberInputProps) => {
    const [localValue, setLocalValue] = useState<string>(value.toString());

    useEffect(() => {
        setLocalValue(value.toString());
    }, [value]);

    const handleCommit = () => {
        let val = Number(localValue);
        if (isNaN(val) || localValue.trim() === "") {
            val = value;
        }
        
        val = Math.min(max, Math.max(min, val));
        
        setLocalValue(val.toString());
        if (val !== value) {
            onChange(val);
        }
    };

    return (
        <input
            type="number"
            min={min}
            max={max}
            step={step}
            value={localValue}
            style={style}
            onChange={(e) => setLocalValue(e.target.value)}
            onBlur={handleCommit}
            onKeyDown={(e) => {
                if (e.key === "Enter") {
                    handleCommit();
                }
            }}
        />
    );
};
