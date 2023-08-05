"""
Napalm driver for ArubaOS 505 Wi-Fi Device using SSH.
Read https://napalm.readthedocs.io for more information.
"""

from napalm.base import NetworkDriver
from napalm.base.exceptions import (
    ConnectionException,
    SessionLockedException,
    MergeConfigException,
    ReplaceConfigException,
    CommandErrorException,
    )


import paramiko
import time

hp_manufacture = '5406zl'
hp_platform = "HP"
cisco_fttx_platform = "received"

def ssh_connector(hostname, username, password, key=False, timeout=10, port=22):
    """ Connect to remote device and return a channel to use for sending cmds.
        return the returned value is the channel object that will be used to send command to remote device
    """
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username,
                    password=password, look_for_keys=key, timeout=timeout)

    except:
        print("Could not connect to {0}".format(hostname))
        ssh.close()
        return None
    else:
        print("Connected to {0}\n".format(hostname))
        channel = ssh.invoke_shell()
        return channel


def send_single_cmd(cmd, channel, incoming_sleep_time=4, out_going_sleep_time=4):
    """Send cmd via the channel if channel object is not None
        return: the return value is the result or the executed cmd
    """
    if not cmd:
        print(f"Not command to send\n")
        return None
    if not channel:
        print(f"No channel available\n")
        return None

    banner = channel.recv(99999).decode("utf-8")
    time.sleep(1)
    print(f"{banner}\n\n")
    time.sleep(1)

    channel.send(cmd + "\n")
    time.sleep(out_going_sleep_time)

    output = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    return output


class ArubaOS505(NetworkDriver):
    """Napalm driver for ArubaOS 505 Wi-Fi Device."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Initializer."""

        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout

        #self.platform = "ArubaOS"
        #self.profile = [self.platform]
        self.session_info = None
        self.isAlive = False
        if not optional_args:
            optional_args = {}


    def open(self):
        """
        Implementation of NAPALM method 'open' to open a connection to the device.
        """
        try:
            self.session_info = ssh_connector(hostname=self.hostname,username=self.username,
                                              password=self.password)
            self.isAlive = True
            print(f"connected to {self.hostname}\n\n")
        except ConnectionError as error:
            # Raised if device not available
            #raise ConnectionException(str(error))
            print(f"Failed to connect to {self.hostname}\n\n")


    def close(self):
        """
        Implementation of NAPALM method 'close'. Closes the connection to the device and does
        the necessary cleanup.
        """
        self.isAlive = False
        self.session_info.close()


    def is_alive(self):
        """
        Implementation of NAPALM method 'is_alive'. This is used to determine if there is a
        pre-existing connection that must be closed.
        :return: Returns a flag with the state of the connection.
        """
        return {"is_alive": self.isAlive}

    def get_config(self, retrieve="all", full=False, sanitized=False):
        """
        :return: The object returned is a dictionary with a key for each configuration store:
            - running(string) - Representation of the  running configuration
        """

        configs = {
            "running": "",
            "startup": "No Startup",
            "candidate": "No Candidate"
        }

        if retrieve.lower() in ('running', 'all'):
            command = "show running-config"
            try:
                channel = ssh_connector(self.hostname, self.username, self.password)
            except Exception as e:
                print(f"Failed to interact with: {self.hostname} \n")
                print(e)
            else:
                self.isAlive = True
                output = send_single_cmd(command, channel)
                configs['running'] = output

                data = str(configs['running']).split("\n")
                non_empty_lines = [line for line in data if line.strip() != ""]

                string_without_empty_lines = ""
                for line in non_empty_lines:
                    string_without_empty_lines += line + "\n"
                configs['running'] = string_without_empty_lines
                channel.close()
        if retrieve.lower() in ('startup', 'all'):
            ...

        return configs


def get_lldp_neighbors(self):
    """ArubaOS implementation of 'show ap debug lldp info' """

    interfaces = ["eth0", "eth1", "eth2", "eth3", "eth4"]
    command = "show ap debug lldp info"

    lldp = {"Local Interface": "",
            "Remote Interface": "",
            "Remote Device": "",
            }

    try:
        channel = ssh_connector(self.hostname, self.username, self.password)
    except Exception as e :
        print(f"Failed to interact with: {self.hostname} for LLDP data \n")
        print(e)
    else:
        self.isAlive = True
        output = send_single_cmd(command, channel, incoming_sleep_time=2, out_going_sleep_time=2)
        if output:
            _data = str(output.strip())
            data = _data.split()
            # HP '5406zl'
            if hp_manufacture in _data and hp_platform in _data and "Router" in _data and "Bridge" in _data:
                for int in interfaces:
                    if int == data[1]:
                        lldp_dict = {"port": data[3], "hostname": data[15]}
                        lldp[int] = lldp_dict
                    else:
                        lldp_dict = {"port": "", "hostname": ""}
                        lldp[int] = lldp_dict

            # CISCO FTTX
            elif cisco_fttx_platform in _data and "Router" not in _data and "Not" in _data and "Bridge" in _data:
                for int in interfaces:
                    if int == data[1]:
                        lldp_dict = {"port": data[3], "hostname": data[6]}
                        lldp[int] = lldp_dict
                    else:
                        lldp_dict = {"port": "", "hostname": ""}
                        lldp[int] = lldp_dict

    return lldp