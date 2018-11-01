mapping {
  map sessionId() onto 'sessionId'
  map timestamp() onto 'timestamp'
  map referer() onto 'referer'
  map remoteHost() onto 'remoteHost'
  map eventType() onto 'eventType'
  map location() onto 'location'
  map userAgentString() onto 'userAgent'
  def ua = userAgent()
  map ua.deviceCategory() onto 'userAgentDeviceCategory'
  map ua.deviceCategory() onto 'userAgentDeviceCategory'
  map ua.osFamily() onto 'userAgentOsFamily'
  map ua.osVersion() onto 'userAgentOsVersion'
  map eventParameters().value('id') onto 'id_product'
  map eventParameters().value('price') onto 'price_product'
  map eventParameters().value('total_price') onto 'total_price_product'
  def locationUri = parse location() to uri
  def localUri = parse locationUri.rawFragment() to uri
  map localUri.path() onto 'localPath'
}