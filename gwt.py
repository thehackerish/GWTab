from burp import IBurpExtender
from burp import IMessageEditorTabFactory
from burp import IMessageEditorTab
from burp import IParameter
from gwtparse.GWTParser import GWTParser, Parameter

class BurpExtender(IBurpExtender, IMessageEditorTabFactory):

	def __init__(self):

		self.ext_name = "GWT"

	def	registerExtenderCallbacks(self, callbacks):
		# keep a reference to our callbacks object
		self._callbacks = callbacks
		
		# obtain an extension helpers object
		self._helpers = callbacks.getHelpers()
		
		# set our extension name
		callbacks.setExtensionName("GWTab")
		
		# register ourselves as a message editor tab factory
		callbacks.registerMessageEditorTabFactory(self)

	def createNewInstance(self, controller, editable):
		return GWTParserTab(self, controller, editable)

class GWTParserTab(IMessageEditorTab):
	def __init__(self, extender, controller, editable):
		self._extender = extender
		self._editable = editable
		self._helpers = extender._callbacks.getHelpers()
		self._txtInput = extender._callbacks.createTextEditor()
		self._txtInput.setEditable(editable)

	def getTabCaption(self):
		return "GWT"
		
	def getUiComponent(self):
		return self._txtInput.getComponent()
		
	def isEnabled(self, content, isRequest):
		# enable this tab for requests containing a data parameter
		return self.isGWTData(content, isRequest)

	def isGWTData(self, content, isRequest):
		if isRequest:
			offset = self._helpers.analyzeRequest(content).getBodyOffset()
			body = self._helpers.bytesToString(content)[offset:]
			if body:
				return "|0|" in body[1:4]
		return False
		
	def setMessage(self, content, isRequest):

		if content is None:
			# clear our display
			self._txtInput.setText(None)
			self._txtInput.setEditable(False)
		
		else:
			offset = self._helpers.analyzeRequest(content).getBodyOffset()
			body = self._helpers.bytesToString(content)[offset:]

			self._txtInput.setText(self._helpers.stringToBytes(self.parseGWT(body)))
			self._txtInput.setEditable(self._editable)
		
		# remember the displayed content
		self._currentMessage = content

	def parseGWT(self, data):
		try:
			gwt = GWTParser()
			gwt.burp = True
			gwt.deserialize(data)
			return gwt.get_fuzzstr()
		except:
			return "Parser failed"
	
	def getMessage(self):
		return self._currentMessage
	
	def isModified(self):
		return self._txtInput.isTextModified()
	
	def getSelectedData(self):
		return self._txtInput.getSelectedText()
