local obj = {}
obj.__index = obj

obj.logger = hs.logger.new('arrange')

obj.configFile = hs.spoons.scriptPath() .. "config.json"

obj.arrangements = {}


local menuItems = {}
menubar = hs.menubar.new()
menubar:setTitle("🖥")
menuItems = arrangeDesktop:addMenuItems(menuItems)
menubar:setMenu(menuItems)


function obj:_writeConfiguration(config)
    return hs.json.write(config, obj.configFile, true, true)
end


function obj:_loadConfiguration()
    local config = {}
    local fileExists = hs.fs.displayName(obj.configFile)

    if fileExists == nil then
        if obj._writeConfiguration(config) == false then
            obj.logger.e("Unable to write out initial configuration file.")
            return nil
        end
    else
        config = hs.json.read(obj.configFile)
        if config == nil then
            return nil
        end
    end

    return config
end


function obj:_buildArrangement()
    local arrangement = {}
    for _, v in pairs(hs.screen.allScreens()) do
        local monitorUUID = v:getUUID()

        arrangement[monitorUUID] = {}
        arrangement[monitorUUID]['Monitor Name'] = v:name()
        arrangement[monitorUUID]['apps'] = {}

        local windows = hs.window.filter.new(true):setScreens(v:getUUID()):getWindows()
        for k, wv in pairs(windows) do
            arrangement[monitorUUID]['apps'][wv:application():title()] = {}

            wv:focus()

            if k == 1 then
                local buttonPressed, name = hs.dialog.textPrompt("Name this monitor", "", v:name(), "OK", "Cancel")
                if buttonPressed == "OK" and name ~= "" then
                    arrangement[monitorUUID]['Monitor Name'] = name
                end
            end

            for i, t in pairs(wv:frame()) do
                local attribute = string.gsub(i, '_', '')
                arrangement[monitorUUID]['apps'][wv:application():title()][attribute] = t
            end
        end
    end

    return arrangement
end


function obj:createArrangement()
    local config = obj:_loadConfiguration()

    local buttonPressed, arrangementName = hs.dialog.textPrompt("Name this arrangement:", "", "Desk", "OK", "Cancel")
    if buttonPressed == "Cancel" then
        return
    end

    hs.dialog.blockAlert(
    	"We will now record each of your application windows.", 
    	"Each will window will flash into focus. \
    	The first focus on each monitor will prompt you to name the monitor."
	)

    config[arrangementName] = obj:_buildArrangement(arrangementName)

    written = obj:_writeConfiguration(config)
    if written == false then
        hs.dialog.blockAlert("We could not create the config.json file.", "", "OK")
        return
    end

    hs.dialog.blockAlert("Your arrangement has been saved!", "Check config.json for any duplicates.", "OK")
end


function obj:_positionApp(app, appTitle, screen, frame)
    obj.logger.d('Positioning ' .. appTitle)

    app:activate()
    local windows = hs.window.filter.new(appTitle):getWindows()

    for _, v in pairs(windows) do
        obj.logger.d('  moving window ' .. v:id() .. ' of app ' .. appTitle)
        v:moveToScreen(screen)
        v:setFrame(frame, 0)
    end
end


function obj:arrange(arrangement)
    for monitorUUID, monitorDetails in pairs(obj.arrangements[arrangement]) do
        if hs.screen.find(monitorUUID) ~= nil then
            for appName, position in pairs(monitorDetails['apps']) do
                app = hs.application.get(appName)
                if app ~= nil then
                    obj:_positionApp(app, appName, monitorUUID, position)
                end
            end
            if monitorDetails['top_apps'] then
                for appName, position in pairs(monitorDetails['top_apps']) do
                    app = hs.application.get(appName)
                    if app ~= nil then
                        obj:_positionApp(app, appName, monitorUUID, position)
                    end
                end
            end
        end
    end
end


function obj:addMenuItems(menuItems)
    if menuItems == nil then
        menuItems = {}
    end

    table.insert(menuItems, { title = "Create Desktop Arrangement", fn = function() obj:createArrangement() end })
    table.insert(menuItems, { title = "-" })

    local next = next
    obj.arrangements = obj:_loadConfiguration()
    if next(obj.arrangements) ~= nil then
        for k, _ in pairs(obj.arrangements) do
            table.insert(menuItems, { title = k, fn = function() obj:arrange(k) end })
        end
    end

    return menuItems
end


return obj