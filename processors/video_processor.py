import os

from data_models import Story

import moviepy.editor as mpy


class VideoProcessor:
	FILENAME: str = "final_video.mp4"
	FPS: int = 24
	AUDIO_GAP: float = 1.0
	FRAME_EXPLANATION_DURATION: int = 4
	FRAME_START_DURATION: int = 4
	FRAME_END_DURATION: int = 4

	def generate_video(self, workdir: str, story: Story) -> str:
		"""
		Create a video for the given story
		:return: local filepath for the generated video
		"""
		page_clips = []
		audio_clips = []
		current_start = 0
		for i in range(len(story.pages)):
			page = story.pages[i]
			page_clip = mpy.ImageClip(page.page_filepath).set_duration(page.audio.length_in_seconds + self.AUDIO_GAP)
			page_clips.append(page_clip)
			audio_clip = mpy.AudioFileClip(story.pages[i].audio.mp3_file).set_start(current_start)
			audio_clips.append(audio_clip)
			# keep track of the current length
			current_start += page.audio.length_in_seconds + self.AUDIO_GAP

		clip_filepath = os.path.join(workdir, self.FILENAME)
		clip = mpy.concatenate_videoclips(page_clips, method="compose")
		clip.audio = mpy.CompositeAudioClip(audio_clips)

		start_frame_clip = mpy.ImageClip(story.start_page_filepath).set_duration(self.FRAME_START_DURATION)
		end_frame_clip = mpy.ImageClip(story.end_page_filepath).set_duration(self.FRAME_END_DURATION)
		final_clip = mpy.concatenate_videoclips([start_frame_clip, clip, end_frame_clip], method="compose")
		final_clip.write_videofile(clip_filepath, fps=self.FPS)
		return clip_filepath