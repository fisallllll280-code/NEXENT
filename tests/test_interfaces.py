from nexent.interfaces import InterfaceKind, Platform, default_manifest


def test_default_manifest_covers_all_operational_surfaces():
    manifest = default_manifest()

    assert {item.platform for item in manifest} == {
        Platform.LINUX,
        Platform.WINDOWS,
        Platform.ANDROID,
        Platform.DESKTOP,
        Platform.WEB,
    }


def test_android_uses_mobile_interface():
    android = next(item for item in default_manifest() if item.platform is Platform.ANDROID)
    assert android.kind is InterfaceKind.MOBILE
    assert "https" in android.transport


def test_all_interfaces_share_the_same_core_contract():
    manifest = default_manifest("https://nexent.local")
    assert {item.core_endpoint for item in manifest} == {"https://nexent.local"}
    assert all("governance" in item.capabilities for item in manifest)
    assert all("evidence" in item.capabilities for item in manifest)
