﻿import { jsPDF } from "jspdf"
var callAddFont = function () {
this.addFileToVFS('times-normal.ttf', font);
this.addFont('times-normal.ttf', 'customTimes', 'normal');
};
jsPDF.API.events.push(['addFonts', callAddFont])