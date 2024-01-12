import os

# Returns if the specified drive has a valid video DVD inserted
def is_dvd_drive(drive):
    # Check if a media files exists currently in the drive
    sample_file_path = os.path.join(drive, 'VIDEO_TS', 'VIDEO_TS.IFO')
    return os.path.exists(sample_file_path)

# Returns all possible Windows drives that contain a video DVD inserted
def get_dvd_drives():
    # Get every drive letter
    drives = ['%s:\\' % d for d in 'ABCDEFGHIJKLMNOPQURSTUVWXYZ']
    
    # Blacklist for drives that are dvd drives
    dvd_drives = [drive for drive in drives if is_dvd_drive(drive)]
    return dvd_drives