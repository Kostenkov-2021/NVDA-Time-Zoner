import threading
import os.path
import sys
import globalPluginHandler
from scriptHandler import getLastScriptRepeatCount
from scriptHandler import script
import globalCommands
from globalCommands import GlobalCommands as Scripts
import ui
import speech
from datetime import datetime
pythonVersion = int(sys.version[:1])
# Here, we use the Python2 or 3 versions of pytz
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), "modules", "2" if pythonVersion == 2 else "3"))
from pytz import timezone, common_timezones
from tzlocal import get_localzone
del sys.path[0]
import gui
import wx
from gui import SettingsDialog, guiHelper
import json
from time import sleep

class SpeakThread(threading.Thread):
	def __init__(self, repeatCount, destTimezones):
		threading.Thread.__init__(self)
		self.repeatCount = repeatCount
		self.interrupted = False
		self.destTimezones = destTimezones

	def getTimezone(self):
		l = len(self.destTimezones)
		if l == 0:
			return ""
		return self.destTimezones[self.repeatCount%l]

	def sayInTimezone(self):
		selectedTz = self.getTimezone()
		if selectedTz == "":
			ui.message("No timezones set")
			return
		dateFormat = "%A, %B %#d, %Y"
		timeFormat = "%#I:%M %p %Z"
		now = datetime.now(timezone("UTC"))		
		destTimezone = now.astimezone(timezone(selectedTz))
		# By the time the code gets down here, we could have signaled this thread to terminate.
		# This will be the case if retrieval is taking a long time and we've pressed the key multiple times to get successive information in our timezone ring, in which case this thread is marked dirty.
		if self.interrupted:
			return
		ui.message("%s, %s" % (destTimezone.strftime(timeFormat), destTimezone.strftime(dateFormat)))

	def run(self):
		self.sayInTimezone()

class TimezoneSelectorDialog(wx.Dialog):
	def __init__(self, parent, globalPluginClass):
		super(wx.Dialog, self).__init__(parent, title="Configure Timezone Ring")
		self.gPlugin = globalPluginClass
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		self.filterElement = sHelper.addLabeledControl("Filter:", wx.TextCtrl)
		# The label and text box will be next to each other.
		# Below this we will find the label and listbox.
		self.timezonesList = sHelper.addLabeledControl("Timezones (select to add, deselect to remove)", wx.ListBox, choices=common_timezones, style=wx.LB_MULTIPLE)
		self.timezonesList.Bind(wx.EVT_LISTBOX, self.onTimezoneSelected)
		self.selectedTimezonesList = sHelper.addLabeledControl("Timezone Ring", wx.ListBox, choices=[])
		self.selectedTimezonesList.AppendItems(self.gPlugin.destTimezones)
		self.setTimezonesListSelections()
		# The label and listbox will be below each other
		self.filterElement.Bind(wx.EVT_TEXT, self.onFilterTextChange)
		removeButton = sHelper.addItem( wx.Button(self, label="Remove"))
		removeButton.Bind(wx.EVT_BUTTON, self.onRemoveClick)
		moveUpButton = sHelper.addItem( wx.Button(self, label="Move Up"))
		moveUpButton.Bind(wx.EVT_BUTTON, self.onMoveUp)
		moveDownButton = sHelper.addItem( wx.Button(self, label="Move Down"))
		moveDownButton.Bind(wx.EVT_BUTTON, self.onMoveDown)
		setButton = sHelper.addItem( wx.Button(self, label="Save"))
		setButton.Bind(wx.EVT_BUTTON, self.onSetTZClick)
		cancelButton = sHelper.addItem( wx.Button(self, label="Cancel"))
		cancelButton.Bind(wx.EVT_BUTTON, self.onCancelClick)
		# TODO: Right now, the buttons are stacked. We should put them next to each other.

	def isMovable(self):
		index = self.selectedTimezonesList.GetSelection()
		numItems = self.selectedTimezonesList.GetCount()
		if index == wx.NOT_FOUND or numItems < 2:
			return False
		return True

	def onMoveUp(self, event):
		if not self.isMovable():
			return
		index = self.selectedTimezonesList.GetSelection()
		if index == 0:
			return
		tzToMove = self.selectedTimezonesList.GetString(index)
		self.selectedTimezonesList.InsertItems([tzToMove], index-1)
		self.selectedTimezonesList.Delete(index+1)

	def onMoveDown(self, event):
		if not self.isMovable():
			return
		index = self.selectedTimezonesList.GetSelection()
		numItems = self.selectedTimezonesList.GetCount()
		if index == numItems-1:
			return
		tzToMove = self.selectedTimezonesList.GetString(index)
		# We want to insert the item after the one below it, so we have to insert it before index+2
		self.selectedTimezonesList.InsertItems([tzToMove], index+2)
		self.selectedTimezonesList.Delete(index)

	def setTimezonesListSelections(self):
		# We use the selectedTimezonesList here because this is where the user will actively add and remove items.
		# The gPlugin.destTimezones list is only updated on save.
		for tz in self.selectedTimezonesList.GetItems():
			index = self.timezonesList.FindString(tz)
			if index != wx.NOT_FOUND:
				self.timezonesList.SetSelection(index)

	def onRemoveClick(self, event):
		if self.selectedTimezonesList.GetSelection() == wx.NOT_FOUND:
			return
		tzToRemove = self.selectedTimezonesList.GetString(self.selectedTimezonesList.GetSelection())
		self.selectedTimezonesList.Delete(self.selectedTimezonesList.GetSelection())
		indexToRemove = self.timezonesList.FindString(tzToRemove)
		if indexToRemove != wx.NOT_FOUND:
			self.timezonesList.Deselect(indexToRemove)

	def onTimezoneSelected(self, event):
		if event.IsSelection():
			if self.selectedTimezonesList.FindString(event.GetString()) == wx.NOT_FOUND:
				self.selectedTimezonesList.Append(event.GetString())
		else:
			if self.selectedTimezonesList.FindString(event.GetString()) != wx.NOT_FOUND:
				self.selectedTimezonesList.Delete(self.selectedTimezonesList.FindString(event.GetString()))

	# Used to speak the number of filtered results after a delay so that letting up on keys won't interrupt NVDA.
	def announceFilterAfterDelay(self, n):
		sleep(0.5)
		speech.cancelSpeech()
		ui.message("%d results now showing" % n)

	def onFilterTextChange(self, event):
		filterText = self.filterElement.GetValue()
		filtered = []
		if not filterText:
			filtered = common_timezones
		else:
			filterText = filterText.lower()
			filtered = [option for option in common_timezones if filterText in option.lower()]
		self.timezonesList.Set(filtered)
		if len(filtered) > 0:
			self.setTimezonesListSelections()
		# We'll delay the speaking of the filtered results so key presses don't interrupt it.
		t = threading.Thread(target=self.announceFilterAfterDelay, args=[len(filtered)])
		t.start()

	def onSetTZClick(self, event):
		zones = self.selectedTimezonesList.GetItems()
		self.gPlugin.destTimezones = zones
		with open(self.gPlugin.configFile, "w") as fout:
			fout.write(json.dumps({"timezones": zones}))
		self.Destroy()

	def onCancelClick(self, event):
		self.Destroy()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		scriptPath = os.path.realpath(__file__)
		# Place the config file in the aplication that the add-on is in.
		self.configFile = os.path.join(scriptPath[:scriptPath.rindex("\\")], "timezone.json")
		if os.path.isfile(self.configFile):
			with open(self.configFile) as fin:
				data = json.load(fin)
				self.destTimezones = data["timezones"]
		else:
			# We'll try to set the local timezone as the default.
			zone = get_localzone().zone
			if zone not in common_timezones:
				self.destTimezones = []
			else:
				self.destTimezones = [zone]
		self.menu = gui.mainFrame.sysTrayIcon.menu.GetMenuItems()[0].GetSubMenu()
		self.optionsMenu = wx.Menu()
		self.topLevel = self.menu.AppendSubMenu(self.optionsMenu, "Time Zoner", "")
		self.setTZOption = self.optionsMenu.Append(wx.ID_ANY, "Set Timezones...", "Presents a list of timezones")
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.showTimezoneDialog, self.setTZOption)
		self.lastSpeechThread = None

	@script(
		description=_("Speaks the time and date in the specified timezone in the configured timezone ring according to the amount of times this key is pressed in rapid succession."),
		category=globalCommands.SCRCAT_SYSTEM, # Same category as the NVDA speakDateTime script
		gestures=["kb:NVDA+ALT+T"]
	)
	def script_sayTimezoneTime(self, gesture):
		# We'll spawn a new thread here since the first retrieval of the timezone data has a slight delay and it will freeze NVDA for a second or two.
		# First, signal the last thread to die if it's taking too long and we've pressed this key multiple times.
		if self.lastSpeechThread is not None:
			self.lastSpeechThread.interrupted = True
		self.lastSpeechThread = SpeakThread(getLastScriptRepeatCount(), self.destTimezones)
		self.lastSpeechThread.start()

	@script(
		description=_("Brings up the timezone selection dialog."),
		gestures=None
	)
	def script_showTimezoneSelector(self, gesture):
		self.showTimezoneDialog(None)

	def showTimezoneDialog(self, event):
		def createTimezoneDialog():
			dlg= TimezoneSelectorDialog(gui.mainFrame, self)
			dlg.filterElement.SetFocus()
			dlg.Layout()
			dlg.Center(wx.BOTH|wx.Center)
			dlg.Show()
		wx.CallAfter(createTimezoneDialog) # The dialog must be created on the main thread.