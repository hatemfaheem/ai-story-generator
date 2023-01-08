import os

from data_models import Story

import moviepy.editor as mpy


class VideoProcessor:
    _FILENAME: str = "final_video.mp4"
    _FPS: int = 24
    _FRAME_START_DURATION: int = 4
    _FRAME_END_DURATION: int = 4

    """Each page duration is set to the length of the text to speech audio + audio_gap"""
    _AUDIO_GAP: float = 1.0

    def generate_video(self, workdir: str, story: Story) -> str:
        """Create a video for the given story

        Args:
            workdir: The root workdir for the story to generate video for
            story: The story object that contains all details about the story

        Returns: A local filepath for where the created video is stored
        """
        page_clips = []
        audio_clips = []
        current_start = 0
        for i in range(len(story.pages)):
            page = story.pages[i]
            page_clip = mpy.ImageClip(page.page_filepath).set_duration(
                page.audio.length_in_seconds + self._AUDIO_GAP
            )
            page_clips.append(page_clip)
            audio_clip = mpy.AudioFileClip(story.pages[i].audio.mp3_file).set_start(
                current_start
            )
            audio_clips.append(audio_clip)
            # keep track of the current length
            current_start += page.audio.length_in_seconds + self._AUDIO_GAP

        clip_filepath = os.path.join(workdir, self._FILENAME)
        clip = mpy.concatenate_videoclips(page_clips, method="compose")
        clip.audio = mpy.CompositeAudioClip(audio_clips)

        start_frame_clip = mpy.ImageClip(story.start_page_filepath).set_duration(
            self._FRAME_START_DURATION
        )
        end_frame_clip = mpy.ImageClip(story.end_page_filepath).set_duration(
            self._FRAME_END_DURATION
        )
        final_clip = mpy.concatenate_videoclips(
            [start_frame_clip, clip, end_frame_clip], method="compose"
        )
        final_clip.write_videofile(clip_filepath, fps=self._FPS)
        return clip_filepath
