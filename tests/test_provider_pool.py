import os

from smart_search.config import Config


def test_named_provider_pool_order(monkeypatch):
    monkeypatch.delenv("OPENAI_COMPATIBLE_API_URL", raising=False)
    monkeypatch.delenv("OPENAI_COMPATIBLE_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_COMPATIBLE_PROVIDERS", "grok-main,grok-backup")
    monkeypatch.setenv("OPENAI_COMPATIBLE_GROK_MAIN_API_URL", "https://main.example/v1")
    monkeypatch.setenv("OPENAI_COMPATIBLE_GROK_MAIN_API_KEY", "main-key")
    monkeypatch.setenv("OPENAI_COMPATIBLE_GROK_MAIN_MODEL", "grok-a")
    monkeypatch.setenv("OPENAI_COMPATIBLE_GROK_BACKUP_API_URL", "https://backup.example/v1")
    monkeypatch.setenv("OPENAI_COMPATIBLE_GROK_BACKUP_API_KEY", "backup-key")
    monkeypatch.setenv("OPENAI_COMPATIBLE_GROK_BACKUP_MODEL", "grok-b")
    cfg = Config()
    providers = cfg.openai_compatible_provider_configs()
    assert [p["provider"] for p in providers] == [
        "openai-compatible:grok-main",
        "openai-compatible:grok-backup",
    ]
    assert cfg.openai_compatible_api_url == "https://main.example/v1"
    from smart_search.service import _main_search_fallback_chain, _main_search_provider_configs

    chain = _main_search_fallback_chain()
    assert chain[1:] == ["openai-compatible:grok-main", "openai-compatible:grok-backup"]
    configs = _main_search_provider_configs()
    assert [c["provider"] for c in configs] == [
        "openai-compatible:grok-main",
        "openai-compatible:grok-backup",
    ]
