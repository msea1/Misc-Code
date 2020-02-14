tell application "Photos"
	set photo_obj to get selection -- Get the selected photo
	try
		if photo_obj is {} then error -- No selection
	on error
		display alert "Select a photo, then run this script to find albums containing the photo."
		return
	end try
	
	set photo_id to get id of first item in photo_obj
	
	-- look through top level album(s)
	set album_names to name of albums whose id of media items contains photo_id
	if album_names is not {} then
		display dialog "Photo Found in album(s) " & album_names
		return
	end if
	
	-- dive into folders
	-- TODO rewrite as DFS using .scpt weird syntax
	---- repeat while count (folders in this_folder) > 0
	---- end repeat
	repeat with i from 1 to count (folders)
		set this_folder to item i of folders
		my check_level(photo_id, this_folder)
		repeat with j from 1 to count (folders in this_folder)
			set dive_folder to item j of folders in this_folder
			my check_level(photo_id, dive_folder)
			repeat with k from 1 to count (folders in dive_folder)
				set dive2_folder to item k of folders in dive_folder
				my check_level(photo_id, dive2_folder)
			end repeat
		end repeat
	end repeat
	display dialog "Done checking albums"
end tell

on check_level(photo_id, container_obj)
	tell application "Photos"
		set album_names to name of albums in container_obj whose id of media items contains photo_id
		if album_names is not {} then
			display dialog "Photo Found in album(s) " & album_names
			return
		end if
	end tell
end check_level

