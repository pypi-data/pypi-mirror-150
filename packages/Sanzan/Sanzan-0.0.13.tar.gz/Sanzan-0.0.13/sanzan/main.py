from .etc import *
import os


class _Cryptor:
    def __init__(self, ipath) -> None:
        self.ipath = ipath
        self.shuf_order = None
        self.out = None

        # TODO: Handle url stream
        if self.ipath.startswith("http"):
            pass
        # Path is a file
        else:
            if not os.path.isfile(self.ipath):
                raise FileNotFoundError(f"No such input file: '{self.ipath}'")
            self.cap = cv2.VideoCapture(self.ipath)
            print(f"Opened file: {os.path.basename(self.ipath)}")

        self.props = get_properties(self.cap)

    def set_output(self, path=None):
        self.out = cv2.VideoWriter(
            path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            self.props["fps"],
            (int(self.props["width"]), int(self.props["height"])),
            isColor=True,
        )
        if not self.out.isOpened():
            raise OSError("Invalid output path or file format specified")
        print(f"Writing to: {path}")

        return self

    def _gen_key(self, height, password=None):
        shuf_order = np.arange(int(height))
        if password:
            np.random.seed(bytearray(password, encoding="utf8"))
            print(f"Generating key with password")
        np.random.shuffle(shuf_order)
        if password:
            np.random.seed()

        return shuf_order


class Encryptor(_Cryptor):
    def gen_key(self, path=None, password=None):
        if type(self.shuf_order) is np.ndarray:
            raise SZException("`gen_key` was called twice!")

        self.shuf_order = super()._gen_key(height=self.props["height"], password=password)

        if not path:
            path = f"{self.ipath}.key"
        self.shuf_order.tofile(path)
        self.kpath = path

        return self

    def run(self, preview=False, silent=False) -> None:
        if type(self.shuf_order) is not np.ndarray:
            raise SZException("No key found. Use `gen_key` to generate a key first.")

        print(f"Encrypting with keyfile {os.path.basename(self.kpath)}")

        for i in tqdm(range(int(self.props["frames"])), disable=silent):
            success, frame = self.cap.read()
            if not success:
                print(f"Failed to read frame {i}!")
                break

            frame_arr = np.array(frame, dtype=np.uint8)
            frame_arr = frame_arr[self.shuf_order]

            if self.out:
                self.out.write(frame_arr)
            if preview:
                cv2.imshow(self.ipath, frame_arr)
                cv2.waitKey(1)

        self.cap.release()
        if self.out:
            self.out.release()


class Decryptor(_Cryptor):
    def __init__(self, ipath):
        self.unshuf_order = None
        super().__init__(ipath)

    def set_key(self, path=None, password=None):
        if type(self.unshuf_order) is np.ndarray:
            raise SZException("`set_key` was called twice!")

        if path and password:
            raise SZException("Both keypath and password were specified!")

        self.kpath = path

        if self.kpath:
            self.shuf_order = np.fromfile(self.kpath, dtype="int")
            print(f"Decrypting with keyfile {os.path.basename(self.kpath)}")
        elif password:
            self.shuf_order = super()._gen_key(height=self.props["height"], password=password)
        else:
            raise SZException("No keypath or password specifed.")

        self.unshuf_order = np.zeros_like(self.shuf_order)
        self.unshuf_order[self.shuf_order] = np.arange(int(self.props["height"]))

        return self

    def run(self, preview=False, silent=False) -> None:
        if type(self.unshuf_order) is not np.ndarray:
            # try_kpath = f"{self.ipath}.key"
            # print(f"`set_key` was not used. Trying default path {try_kpath}.")
            # self.set_key(try_kpath)
            raise SZException("No key found. Use `set_key` to set a key first.")

        for i in tqdm(range(int(self.props["frames"])), disable=silent):
            success, frame = self.cap.read()
            if not success:
                print(f"Failed to read frame {i}!")
                break

            frame_arr = np.array(frame, dtype=np.uint8)
            frame_arr = frame_arr[self.unshuf_order]

            if self.out:
                self.out.write(frame_arr)
            if preview:
                cv2.imshow(self.ipath, frame_arr)
                cv2.waitKey(1)

        self.cap.release()
        if self.out:
            self.out.release()