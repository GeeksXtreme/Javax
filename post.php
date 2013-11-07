
<?php
$data = "";
$fd = @fopen("/tmp/captured_forms.txt", "a");
$data = date("Y-m-d H:i:s") . "\t" . " IP:" . $_SERVER['REMOTE_ADDR'] . "\t";
$data = $data . $_GET['referanceMod'] . "\n\n";
fwrite($fd, $data);
fclose($fd);
?>
<html>
<head>
	<meta http-equiv="refresh" content="55;url=http://0.0.0.0" />
	<script type="text/javascript" src="PluginDetect.js"></script>
	<script type="text/JavaScript">
	function timedRefresh(timeoutPeriod) {
		setTimeout("location.reload(true);",timeoutPeriod);
	}
	</script>
</head>
<body onload="JavaScript:timedRefresh(15000);">
	<script type="text/javascript">
	var jver = PluginDetect.getVersion("Java");
	var aver = PluginDetect.getVersion('Flash');
	var plg2 = PluginDetect.getVersion('AdobeReader');
	var plg3 = PluginDetect.getVersion('QuickTime');
	var plg4 = PluginDetect.getVersion('RealPlayer');
	var plg5 = PluginDetect.getVersion('Shockwave');
	var plg6 = PluginDetect.getVersion('Silverlight');
	var plg7 = PluginDetect.getVersion("WindowsMediaPlayer");
	var iscrm = PluginDetect.isChrome;
	var iever = PluginDetect.verIE;
	var plg8 = PluginDetect.verOpera; 
	var plg12 = PluginDetect.OS;
	var plg13 = PluginDetect.isIE;
	var plg14 = PluginDetect.ActiveXEnabled;
	var plg16 = PluginDetect.verIEfull;
	var plg17 = PluginDetect.docModeIE;
	var plg18 = PluginDetect.isGecko;
	var plg19 = PluginDetect.verGecko;
	var plg20 = PluginDetect.isSafari;
	var plg21 = PluginDetect.verSafari;
	var plg23 = PluginDetect.verChrome;
	var plg24 = PluginDetect.isOpera;
	var plg9 = navigator.platform;
	var plg0 = navigator.javaEnabled();
	var plg11 = navigator.cookieEnabled; 
	var plg25 = navigator.userAgent;
	document.write("PLATFORM: "+ plg9);
	document.write("<br />");
	document.write("JAVA VERSION: " + jver);
	document.write("<br />");
