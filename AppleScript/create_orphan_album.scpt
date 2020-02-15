tell application "Photos"
	set photos_seen to id of media items in albums
	
	repeat with i from 1 to count (folders)
		set this_folder to item i of folders
		set photos_seen to photos_seen & my check_level(this_folder)
		
		-- 2nd level
		repeat with j from 1 to count (folders in this_folder)
			set dive_folder to item j of folders in this_folder
			set photos_seen to photos_seen & my check_level(dive_folder)
			
			-- 3rd level
			repeat with k from 1 to count (folders in dive_folder)
				set dive2_folder to item k of folders in dive_folder
				set photos_seen to photos_seen & my check_level(dive2_folder)
			end repeat
		end repeat
	end repeat
	
	-- list of all items, anywhere
	set potential_orphans to media items
	set true_orphans to {}
	
	repeat with i from 1 to count of potential_orphans
		set is_orphan to item i in potential_orphans
		set check_id to id of is_orphan
		if photos_seen does not contain check_id then set end of true_orphans to is_orphan
	end repeat
	
	-- create new album out of remaining ids
	set new_album to make new album named "Orphaned"
	add true_orphans to new_album
	
end tell

on check_level(container_obj)
	set photos_in_level to {}
	tell application "Photos"
		repeat with i from 1 to count (albums in container_obj)
			set this_album to item i of albums in container_obj
			set photos_in_level to photos_in_level & id of media items in this_album
		end repeat
	end tell
	return photos_in_level
end check_level

