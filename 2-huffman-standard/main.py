import heapq
import os
import json

class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __eq__(self, other):
        return self.freq == other.freq

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    # functions for compression:

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            node = HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while (len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if (root is None):
            return

        if (root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if (len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r', encoding='utf-8') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)

            # write the header containing the codes dictionary
            codes_bytes = json.dumps(self.codes).encode('utf-8')
            header_size_bytes = len(codes_bytes).to_bytes(4, byteorder='big')
            output.write(header_size_bytes + codes_bytes)

            # write the encoded text
            output.write(bytes(b))

        print("Compressed")
        return output_path
    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if (current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w', encoding='utf-8') as output:
            # read the header containing the codes dictionary
            header_size_bytes = int.from_bytes(file.read(4), byteorder='big')
            header_bytes = file.read(header_size_bytes)
            self.codes = json.loads(header_bytes.decode('utf-8'))

            self.reverse_mapping = {}

            for key, value in self.codes.items():
                self.reverse_mapping[value] = key

            bit_string = ""
            byte = file.read(1)
            while (len(byte) != 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)
            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        print("Decompressed")
        return output_path




import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Huffman-light"
    )
    parser.add_argument("-e", "--encode", help="Encode a text file. output is written to a file named encoded.txt", action="store_true")
    parser.add_argument("-d", "--decode", help="Decode a text file, output is sent to the standard output", action="store_true")
    parser.add_argument("path_to_file")


    args = parser.parse_args()


    if args.encode and args.decode:
        print("Cannot encode and decode at the same time. You can only use one of these options per execution. For help do 'python3 main.py -h")
        exit(1)

    if not args.encode and not args.decode:
        print("Please specify action : encode (-e) or decode (-d). For help do 'python3 main.py -h")

    if args.encode:

        h = HuffmanCoding(args.path_to_file)

        output_path = h.compress()

    elif args.decode:
        h = HuffmanCoding(args.path_to_file)
        output_path = h.decompress(h.path)
