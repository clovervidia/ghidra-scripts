#Base64 decodes the currently selected string and adds the decoded string as an EOL comment
#@author clover v.
#@category Strings

import base64
from ghidra.program.model.listing import CodeUnit

def main():
	# If something is highlighted, use its minimum address, otherwise use whatever the current address is.
	if currentSelection:
		b64_string_address = currentSelection.getMinAddress()
	else:
		b64_string_address = currentAddress

	# A Listing is needed to get the defined data and set the comment.
	listing = currentProgram.getListing()

	# listing.getDefinedDataAt() returns the defined data at the current address, or None if there isn't any defined data there.
	# Get its default value representation to turn it into a Python string.
	try:
		b64_string = listing.getDefinedDataAt(b64_string_address).getDefaultValueRepresentation()
	except AttributeError:
		print("There's no defined data at {}".format(b64_string_address))
		return

	# If it can't be decoded, it's probably not Base64-encoded text.
	try:
		decoded_string = base64.b64decode(b64_string)
	except TypeError:
		print("Couldn't Base64 decode {}.".format(b64_string))
		return

	# Print out the original string as well as the decoded string, and write the decoded string to an EOL comment.
	print('{} -> "{}"'.format(b64_string, decoded_string))
	listing.setComment(b64_string_address, CodeUnit.EOL_COMMENT, decoded_string)

if __name__ == "__main__":
	main()
