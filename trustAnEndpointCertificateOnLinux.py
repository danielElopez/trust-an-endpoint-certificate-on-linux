#  No Warranty or Liability.  The code contained herein is being supplied to Licensee
#  "AS IS" without any warranty of any kind.  OSIsoft DISCLAIMS ALL EXPRESS AND IMPLIED WARRANTIES,
#  INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE and NONINFRINGEMENT. In no event will OSIsoft be liable to Licensee or to any third party
#  for damages of any kind arising from Licensee's use of the this code OR OTHERWISE, including
#  but not limited to direct, indirect, special, incidental and consequential damages, and Licensee
#  expressly assumes the risk of all such damages.  FURTHER, THIS CODE IS NOT ELIGIBLE FOR
#  SUPPORT UNDER EITHER OSISOFT'S STANDARD OR ENTERPRISE LEVEL SUPPORT AGREEMENTS

# Usage:
# 1. Update the host and port constants (below) to reflect your target
# 2. Run this script as root

from socket import socket
import ssl
import os
from sys import argv as command_line_arguments

# Specify the default host name (or FQDN) of your target endpoint, and the port number
TARGET_ENDPOINT_HOST = "lopezpiserver"
TARGET_ENDPOINT_PORT_NUMBER = 8118

# The host name and target endpoint will be overwritten by arguments passed in when running this script
if (len(command_line_arguments) == 3):
    TARGET_ENDPOINT_HOST = command_line_arguments[1]
    TARGET_ENDPOINT_PORT_NUMBER = command_line_arguments[2]

# Specify the path to where the new certificate file will go
target_endpoint_certificate_file_name = TARGET_ENDPOINT_HOST + "_port" + str(TARGET_ENDPOINT_PORT_NUMBER) + ".crt"
target_endpoint_certificate_file_path = "/usr/share/ca-certificates/" + target_endpoint_certificate_file_name

try:
    # Assemble the host and port into an address
    target_endpoint_address = (TARGET_ENDPOINT_HOST, TARGET_ENDPOINT_PORT_NUMBER)

    # Get server certificate that exists at that host and port
    print("Getting certificate from host " + TARGET_ENDPOINT_HOST + " port " + str(TARGET_ENDPOINT_PORT_NUMBER))
    target_endpoint_certificate = ssl.get_server_certificate(target_endpoint_address)
    print("Certificate:")
    print(target_endpoint_certificate)

    # Save that certificate to a file, in "w" mode (overwrite)
    print("Writing certificate to file at location " + target_endpoint_certificate_file_path)
    target_endpoint_certificate_file = open(target_endpoint_certificate_file_path, "w")
    target_endpoint_certificate_file.write(target_endpoint_certificate)
    target_endpoint_certificate_file.close()

    # Update the trusted certificates on your device with this new certificate and print the result
    print("Updating trusted certificates")
    return_code = os.system("sudo update-ca-certificates")
    print("Status of update-ca-certificates: {}".format(return_code))

    # Next, open dpkg-reconfigure to let the user manually accept this cert
    print(
        "\nThis script will next launch sudo dpkg-reconfigure ca-certificates.  Select" +
        "\n'yes' when asked 'Trust new certificates from certificate authorities?'." +
        "\nWhen presented with a list of 'Certificates to activate', use the arrow keys" +
        "\nto highlight the new certificate that you just added; it should be named" +
        "\n'" + target_endpoint_certificate_file_name + "'. Press SPACE to select" +
        "\nthat certificate for activation; once done, there should be a [*] next to" +
        "\nthe certificate. Next, press ENTER to save and apply your changes."
    )
    user_input = input("\nWhen you are finished reading the above instructions, press ENTER to continue.")
    return_code = os.system("sudo dpkg-reconfigure ca-certificates")

    # Script done!
    print("Script complete.")
except Exception as ex:
    # Log any error, if it occurs
    print("Error: " + str(ex))
