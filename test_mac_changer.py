import pytest
import mac_changer


def test_missing_interface(capsys):
    with pytest.raises(SystemExit):
        mac_changer.check_args(None, '00:11:22:33:44:55')
    captured = capsys.readouterr()
    assert captured.out.strip() == 'Please input an interface to change using the "-i" command.\n(Use mac_changer --help for help)'

def test_missing_mac_address(capsys):
    with pytest.raises(SystemExit):
        mac_changer.check_args('eth0', None)
    captured = capsys.readouterr()
    assert captured.out.strip() == 'Please input a MAC address to change to using the "-m" command.\n(Use mac_changer --help for help)'

def test_missing_interface_and_mac_address(capsys):
    with pytest.raises(SystemExit):
        mac_changer.check_args(None, None)
    captured = capsys.readouterr()
    expected_output = """Please input an interface to change using the "-i" command.
(Use mac_changer --help for help)"""
    assert captured.out.strip() == expected_output


