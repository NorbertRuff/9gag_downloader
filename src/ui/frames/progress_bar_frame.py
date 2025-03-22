"""Progress bar frame for displaying download progress.

This frame shows a detailed progress bar with statistics to track the download progress.
"""

import tkinter as tk
from typing import Any, Dict, Optional

import customtkinter as ctk

from src.config import Color, Theme
from src.utils.logging import Logger


class ProgressBarFrame(ctk.CTkFrame):
    """Frame containing a detailed progress bar and download statistics."""

    def __init__(self, master: Any, theme: Theme, **kwargs: Dict[str, Any]):
        """Initialize the progress bar frame.

        Args:
            master: Parent widget.
            theme: Theme configuration.
            **kwargs: Additional keyword arguments to pass to CTkFrame.
        """
        super().__init__(master, **kwargs)
        self.theme = theme
        self.logger_instance = Logger("9GAG Downloader")
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and place the widgets in the frame."""
        # Create container frame with padding
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.BOTH, expand=True
        )

        # Top section with label and percentage
        top_section = ctk.CTkFrame(container, fg_color="transparent")
        top_section.pack(fill=tk.X, pady=(0, self.theme.small_padding))

        # Create progress label
        progress_label = ctk.CTkLabel(
            top_section,
            text="Download Progress:",
            font=self.theme.normal_font,
            text_color=self.theme.text_color,
            anchor="w",
        )

        # Create percentage label
        self.progress_bar_percentage = ctk.CTkLabel(
            top_section,
            text="0%",
            font=self.theme.title_font,
            text_color=self.theme.text_color,
        )

        # Pack top section widgets
        progress_label.pack(side=tk.LEFT)
        self.progress_bar_percentage.pack(side=tk.RIGHT, padx=(10, 0))

        # Progress bar container for styling
        progress_container = ctk.CTkFrame(
            container,
            fg_color=self.theme.progress_background_color,
            corner_radius=self.theme.corner_radius,
            height=self.theme.progress_height,
        )
        progress_container.pack(fill=tk.X, pady=self.theme.small_padding)

        # Create progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_container,
            progress_color=self.theme.progress_color,
            height=self.theme.progress_height - 4,
            corner_radius=self.theme.corner_radius - 2,
            fg_color=self.theme.progress_background_color,
        )
        self.progress_bar.pack(fill=tk.X, expand=True, padx=2, pady=2)
        self.progress_bar.set(0)  # Initialize to 0

        # Create detailed status section
        status_section = ctk.CTkFrame(container, fg_color="transparent")
        status_section.pack(fill=tk.X, pady=self.theme.small_padding)

        # Current item frame
        current_item_frame = ctk.CTkFrame(status_section, fg_color="transparent")
        current_item_frame.pack(fill=tk.X, pady=(self.theme.small_padding, 0))

        # Current item label
        current_item_label = ctk.CTkLabel(
            current_item_frame,
            text="Current Item:",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        current_item_label.pack(side=tk.LEFT)

        # Current item value
        self.current_item_value = ctk.CTkLabel(
            current_item_frame,
            text="None",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        self.current_item_value.pack(side=tk.LEFT, padx=(5, 0))

        # File type indicator
        self.file_type_indicator = ctk.CTkLabel(
            current_item_frame,
            text="",
            font=self.theme.small_font,
            text_color=self.theme.success_color,
            anchor="e",
        )
        self.file_type_indicator.pack(side=tk.RIGHT)

        # Stats frame
        stats_frame = ctk.CTkFrame(status_section, fg_color="transparent")
        stats_frame.pack(fill=tk.X, pady=(self.theme.small_padding, 0))

        # Stats grid
        stats_frame.grid_columnconfigure(0, weight=1)  # Left column
        stats_frame.grid_columnconfigure(1, weight=1)  # Right column

        # Total items
        total_items_label = ctk.CTkLabel(
            stats_frame,
            text="Total Items:",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        total_items_label.grid(row=0, column=0, sticky=tk.W)

        self.total_items_value = ctk.CTkLabel(
            stats_frame,
            text="0",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        self.total_items_value.grid(row=0, column=0, sticky=tk.E, padx=(5, 0))

        # Processed count
        processed_label = ctk.CTkLabel(
            stats_frame,
            text="Processed:",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        processed_label.grid(row=0, column=1, sticky=tk.W, padx=(20, 0))

        self.processed_value = ctk.CTkLabel(
            stats_frame,
            text="0",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        self.processed_value.grid(row=0, column=1, sticky=tk.E, padx=(5, 0))

        # Success count
        success_label = ctk.CTkLabel(
            stats_frame,
            text="Successful:",
            font=self.theme.small_font,
            text_color=self.theme.success_color,
            anchor="w",
        )
        success_label.grid(row=1, column=0, sticky=tk.W)

        self.success_value = ctk.CTkLabel(
            stats_frame,
            text="0",
            font=self.theme.small_font,
            text_color=self.theme.success_color,
            anchor="w",
        )
        self.success_value.grid(row=1, column=0, sticky=tk.E, padx=(5, 0))

        # Failed count
        failed_label = ctk.CTkLabel(
            stats_frame,
            text="Failed:",
            font=self.theme.small_font,
            text_color=self.theme.error_color,
            anchor="w",
        )
        failed_label.grid(row=1, column=1, sticky=tk.W, padx=(20, 0))

        self.failed_value = ctk.CTkLabel(
            stats_frame,
            text="0",
            font=self.theme.small_font,
            text_color=self.theme.error_color,
            anchor="w",
        )
        self.failed_value.grid(row=1, column=1, sticky=tk.E, padx=(5, 0))

        # Already downloaded count
        cached_label = ctk.CTkLabel(
            stats_frame,
            text="Already Downloaded:",
            font=self.theme.small_font,
            text_color=self.theme.info_color,
            anchor="w",
        )
        cached_label.grid(row=2, column=0, sticky=tk.W)

        self.cached_value = ctk.CTkLabel(
            stats_frame,
            text="0",
            font=self.theme.small_font,
            text_color=self.theme.info_color,
            anchor="w",
        )
        self.cached_value.grid(row=2, column=0, sticky=tk.E, padx=(5, 0))

        # Current status
        status_label = ctk.CTkLabel(
            stats_frame,
            text="Status:",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        status_label.grid(row=2, column=1, sticky=tk.W, padx=(20, 0))

        self.status_value = ctk.CTkLabel(
            stats_frame,
            text="Ready",
            font=self.theme.small_font,
            text_color=self.theme.info_color,
            anchor="w",
        )
        self.status_value.grid(row=2, column=1, sticky=tk.E, padx=(5, 0))

        # Media type stats frame
        media_stats_frame = ctk.CTkFrame(status_section, fg_color="transparent")
        media_stats_frame.pack(fill=tk.X, pady=(self.theme.small_padding, 0))

        # Image count
        image_icon = ctk.CTkLabel(
            media_stats_frame,
            text="🖼️",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        image_icon.pack(side=tk.LEFT)

        self.image_count = ctk.CTkLabel(
            media_stats_frame,
            text="0",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        self.image_count.pack(side=tk.LEFT, padx=(2, 15))

        # Video count
        video_icon = ctk.CTkLabel(
            media_stats_frame,
            text="🎬",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        video_icon.pack(side=tk.LEFT)

        self.video_count = ctk.CTkLabel(
            media_stats_frame,
            text="0",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="w",
        )
        self.video_count.pack(side=tk.LEFT, padx=(2, 0))

        # Time estimate
        self.time_estimate = ctk.CTkLabel(
            media_stats_frame,
            text="Est. time: --:--",
            font=self.theme.small_font,
            text_color=self.theme.text_color,
            anchor="e",
        )
        self.time_estimate.pack(side=tk.RIGHT)

        # Create action buttons container
        button_container = ctk.CTkFrame(container, fg_color="transparent")
        button_container.pack(fill=tk.X, pady=(self.theme.padding, 0))

        # Create cancel button
        self.cancel_button = ctk.CTkButton(
            button_container,
            text="Cancel",
            width=self.theme.button_width,
            height=self.theme.button_height,
            font=self.theme.normal_font,
            fg_color=self.theme.button_cancel_color,
            hover_color=self.theme.button_cancel_hover_color,
            text_color=self.theme.button_text_color,
            corner_radius=self.theme.button_corner_radius,
            command=self._cancel_download,
        )

        # Create open log button (initially hidden)
        self.open_log_button = ctk.CTkButton(
            button_container,
            text="Open Log",
            width=self.theme.button_width,
            height=self.theme.button_height,
            font=self.theme.normal_font,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            text_color=self.theme.button_text_color,
            corner_radius=self.theme.button_corner_radius,
            command=self._open_log,
        )

        # Pack buttons
        self.cancel_button.pack(side=tk.LEFT, padx=self.theme.small_padding)

        # Initialize variables for download tracking
        self.total_items = 0
        self.processed_items = 0
        self.successful_items = 0
        self.failed_items = 0
        self.cached_items = 0
        self.image_items = 0
        self.video_items = 0
        self.is_canceled = False

    def _cancel_download(self) -> None:
        """Cancel the current download."""
        self.is_canceled = True
        self.status_value.configure(
            text="Canceling...", text_color=self.theme.warning_color
        )
        self.logger_instance.info("Download canceled by user")

    def pack_open_log_button(self) -> None:
        """Show the open log button."""
        self.open_log_button.pack(
            side=tk.RIGHT, padx=self.theme.small_padding, pady=self.theme.small_padding
        )
        self.cancel_button.pack_forget()  # Hide cancel button when download is complete

    def unpack_open_log_button(self) -> None:
        """Hide the open log button."""
        self.open_log_button.pack_forget()

    def reset_stats(self) -> None:
        """Reset all statistics to zero."""
        self.total_items = 0
        self.processed_items = 0
        self.successful_items = 0
        self.failed_items = 0
        self.cached_items = 0
        self.image_items = 0
        self.video_items = 0
        self.is_canceled = False

        # Update UI
        self.total_items_value.configure(text="0")
        self.processed_value.configure(text="0")
        self.success_value.configure(text="0")
        self.failed_value.configure(text="0")
        self.cached_value.configure(text="0")
        self.image_count.configure(text="0")
        self.video_count.configure(text="0")
        self.current_item_value.configure(text="None")
        self.file_type_indicator.configure(text="")
        self.status_value.configure(text="Ready", text_color=self.theme.info_color)
        self.time_estimate.configure(text="Est. time: --:--")
        self.progress_bar.set(0)
        self.progress_bar_percentage.configure(
            text="0%", text_color=self.theme.text_color
        )

    def set_total_items(self, total: int) -> None:
        """Set the total number of items to download.

        Args:
            total: Total number of items to download.
        """
        self.total_items = total
        self.total_items_value.configure(text=str(total))
        self.status_value.configure(text="Starting", text_color=self.theme.info_color)

    def update_current_item(
        self,
        item_title: str,
        current_index: int,
        is_video: bool = None,
        is_cached: bool = False,
    ) -> None:
        """Update the currently downloading item.

        Args:
            item_title: Title of the current item.
            current_index: Index of the current item.
            is_video: Whether the item is a video or image.
            is_cached: Whether the item was already downloaded.
        """
        # Update the current item label
        self.current_item_value.configure(
            text=f"{item_title} ({current_index + 1}/{self.total_items})"
        )

        # Update file type indicator
        if is_video is not None:
            if is_video:
                self.file_type_indicator.configure(
                    text="Video 🎬", text_color=self.theme.warning_color
                )
            else:
                self.file_type_indicator.configure(
                    text="Image 🖼️", text_color=self.theme.info_color
                )
        else:
            self.file_type_indicator.configure(text="")

        # Update status
        if is_cached:
            self.status_value.configure(
                text="Already Downloaded", text_color=self.theme.info_color
            )
        else:
            self.status_value.configure(
                text="Downloading", text_color=self.theme.success_color
            )

    def increment_counters(
        self,
        success: bool = False,
        failure: bool = False,
        cached: bool = False,
        is_video: bool = False,
    ) -> None:
        """Increment the download counters.

        Args:
            success: Whether to increment the success counter.
            failure: Whether to increment the failure counter.
            cached: Whether to increment the cached counter.
            is_video: Whether the item is a video.
        """
        # Increment processed counter
        self.processed_items += 1
        self.processed_value.configure(text=str(self.processed_items))

        # Increment specific counters
        if success:
            self.successful_items += 1
            self.success_value.configure(text=str(self.successful_items))

            # Increment media type counter
            if is_video:
                self.video_items += 1
                self.video_count.configure(text=str(self.video_items))
            else:
                self.image_items += 1
                self.image_count.configure(text=str(self.image_items))

        if failure:
            self.failed_items += 1
            self.failed_value.configure(text=str(self.failed_items))

        if cached:
            self.cached_items += 1
            self.cached_value.configure(text=str(self.cached_items))

            # For cached items, also increment the media type counter
            if is_video:
                self.video_items += 1
                self.video_count.configure(text=str(self.video_items))
            else:
                self.image_items += 1
                self.image_count.configure(text=str(self.image_items))

    def set_progress_bar(
        self,
        progress_value: float,
        progress_percentage: int,
        color: str = Color.MAIN,
        remaining_time: str = None,
    ) -> None:
        """Update the progress bar and percentage.

        Args:
            progress_value: Progress value between 0 and 1.
            progress_percentage: Progress percentage to display.
            color: Color of the percentage text.
            remaining_time: Estimated remaining time.
        """
        # Ensure progress_value is in the range [0, 1]
        progress_value = max(0, min(1, progress_value))

        # Update progress bar
        self.progress_bar.set(progress_value)

        # Update percentage label
        self.progress_bar_percentage.configure(
            text=f"{progress_percentage}%", text_color=color
        )

        # Update time estimate if provided
        if remaining_time:
            self.time_estimate.configure(text=f"Est. time: {remaining_time}")

        # Update status when complete
        if progress_value >= 1.0:
            self.status_value.configure(
                text="Complete", text_color=self.theme.success_color
            )

        # Update the UI
        self.update()

    def is_download_cancelled(self) -> bool:
        """Check if the download was cancelled by the user.

        Returns:
            True if the download was cancelled, False otherwise.
        """
        return self.is_canceled

    def _open_log(self) -> None:
        """Open the log file."""
        self.logger_instance.open_log_file()
