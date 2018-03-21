'use strict';
export const navHeight: number = 50;
export const pages: Array<string> = ["players", "teams","games"];
export const numPages: number = pages.length;
export const secondsToGametime = (totalSeconds) => {
  if (Math.abs(totalSeconds) > 1200) {
    var s = Math.abs(totalSeconds) - 20*60;
    var minutes = Math.floor(s / 60);
    var seconds = s % 60;
    if (minutes < 10) {minutes = '0'+ minutes;}
    if (seconds < 10) {seconds = '0'+ seconds;}
    return minutes+':'+seconds
  }
  var s = Math.abs(totalSeconds);
  var minutes = Math.floor(s / 60);
  var seconds = s % 60;
  if (minutes < 10) {minutes = '0'+ minutes;}
  if (seconds < 10) {seconds = '0'+ seconds;}
  return minutes+':'+seconds;
}
export const gametimeToSeconds = (gametime, isSecondHalf) => {
  var minSec = gametime.split(":");
  if (isSecondHalf) return parseInt(minSec[0])*60 + parseInt(minSec[1]);
  return parseInt(minSec[0])*60 + parseInt(minSec[1]) + 1200;
}
