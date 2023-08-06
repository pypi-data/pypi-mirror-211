from moviepy.editor \
    import VideoFileClip

from operators.counter \
    import Counter

from os.path \
    import \
    isdir, \
    isfile, \
    join

from math \
    import \
    floor, \
    ceil


class Extractor:
    def __init__(
            self,
            save_location: str,
            path_to_video: str,
            save_frames_as: str = 'jpg'
    ):
        self.counter = Counter()

        self.save_location: str = save_location
        self.path_to_video: str = path_to_video

        self.video_clip: None | VideoFileClip = None
        self.save_frames_as_format: str = save_frames_as

        self.debug_mode: bool = True
        self.snapshot_at: float = 1.0

    def __del__(self):
        if not (self.video_clip is None):
            self.video_clip.close()

    def debug_show_location_message(
            self,
            message: str,
            location: str
    ):
        if self.debug_mode:
            print(
                message,
                ':',
                location
            )

    def execute(self):
        if self.exist_video_file() \
           and \
           self.exist_save_location():

            self.debug_show_location_message(
                'found video',
                self.get_path_to_video()
            )

            self.debug_show_location_message(
                'found save location',
                self.get_save_location()
            )
        else:
            return

        self.set_video_clip(
            VideoFileClip(
                self.get_path_to_video()
            )
        )

        self.process_video()

    def process_video(self):
        counter_of_frames = self.get_counter()

        duration_of_video = floor(
            self.get_video_clip().duration
        )

        for frame_at in \
                range(
                    1,
                    duration_of_video
                ):

            self.get_video_clip().save_frame(
                str(
                    join(
                        self.get_save_location(),

                        counter_of_frames.get_value_as_string() + '.' + self.get_save_frames_as_format()
                    )
                ),

                t = frame_at
            )

            counter_of_frames.increment()






    def exist_video_file(self) -> bool:
        return isfile(
            self.path_to_video
        )

    def exist_save_location(self) -> bool:
        return isdir(
            self.get_save_location()
        )

    def get_counter(
            self
    ) -> Counter:
        return self.counter

    def get_save_location(
            self
    ) -> str:
        return self.save_location

    def get_path_to_video(
            self
    ) -> str:
        return self.path_to_video

    def get_video_clip(
            self
    ) -> None | VideoFileClip:
        return self.video_clip

    def get_save_frames_as_format(
            self
    ) -> str:
        return self.save_frames_as_format

    def set_save_frames_as_format(
            self,
            value: str
    ) -> None:
        self.save_frames_as_format = value

    def set_counter(
            self,
            value: Counter
    ) -> None:
        self.counter = value

    def set_save_location(
            self,
            value: str
    ) -> None:
        self.save_location = value

    def set_path_to_video(
            self,
            value: str
    ) -> None:
        self.path_to_video = value

    def set_video_clip(
            self,
            value: VideoFileClip | None
    ) -> None:
        self.video_clip = value

