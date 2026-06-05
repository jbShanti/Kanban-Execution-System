from pathlib import Path
from typing import Any, TypeAlias, cast

import yaml

ScoringConfig: TypeAlias = dict[str, Any]

def load_scoring_config(path: Path) -> ScoringConfig:
    config = yaml.safe_load(path.read_text())

    if not isinstance(config, dict):
        raise ValueError("scoring.yaml must contain a YAML mapping")

    return cast(ScoringConfig, config)