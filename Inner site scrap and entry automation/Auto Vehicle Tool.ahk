+Escape::
ExitApp
return

NumpadSub::Pause ;Default F12 - NumpadSub for easier access (autoclicker)
return

;------ Hotkeys/Macros -----

;------- Excel hotkeys -------

F5:: ;Click excel -> check path if empty
SendMode Input
SendInput {Enter}
sleep 2000
loop, 4
{
SendInput {right}
}
SendInput !n
sleep 200
SendInput {a}{j}
SendInput {PgDn}
return

F6:: ; Close excel
SendMode Input
SendInput !{F4}
SendInput {Right}
SendInput {Enter}
sleep 1000
SendInput {Right}
return

;------- Shortcuts insert manually -------

;------- AutoClicker - Infinite Loop, Pause F12 or Shift+Esc -------

F11::
;SendMode Input

loop
{
;Click
SendInput !{r}
Sleep 50
}
Return

;------- Search folder -------

`:: ;ctrl+f plus more, for searching image within folder
SendMode Input
;---
WinActivate , "Άνοιγμα"
WinGetActiveTitle, title
While % title != "Άνοιγμα"
{
WinActivate , "Άνοιγμα"
WinGetActiveTitle, title
}
SendInput ^f
SendInput ^v
sleep 1100
SendInput {Tab}
SendInput {Tab}
SendInput {Tab}
SendInput {Right}
SendInput {Left}
Keywait, NumpadEnter, D
SendInput {Enter}
return

;------- Recycle shortcuts -------


F1:: ;Recycle code select
Coordmode, Mouse, Relative
SendMode Input
BlockInput, MouseMove
;---Commands---
WinActivate, ahk_exe chrome.exe
WinActive, ("ahk_exe chrome.exe")
Click 1
MouseMove 250, 190
sleep 200
Click, 2
SendInput ^c
Clipwait, 2
sleep 100 ;Very  inconsistent without it
WinActivate, ahk_exe notepad++.exe
WinActive, ("ahk_exe notepad++.exe")
SendInput ^f
SendInput ^v
SendInput {Enter}
;---
BlockInput, MouseMoveOff
return


Tab:: ;Copy subcode, Changed from Tab to not interfer with other hotkeys
SendMode Input
Click, 2
SendInput ^c
Clipwait
return

;----- Navigation hotkeys for site -----

!W::
WinActivate, ahk_exe chrome.exe
WinActive, ("ahk_exe chrome.exe")
Coordmode, Mouse, Relative
SendMode Input
Click 640, 155 ; to proto einai: de3ia - aristera [- aristera + de3ia]
return

!A::
WinActivate, ahk_exe chrome.exe
WinActive, ("ahk_exe chrome.exe")
Coordmode, Mouse, Relative
SendMode Input
Click 14, 570
return

!D::
WinActivate, ahk_exe chrome.exe
WinActive, ("ahk_class Chrome_WidgetWin_1")
Coordmode, Mouse, Relative
SendMode Input
Click 1031, 568
return

;------- Code Base -------

;--- Browser step back a page
BrowserBack()
{
Sleep 2000
SendInput !{Left}
Sleep 2000
return
}



;---Moving menu ---
MovingRight()
{
Sleep 3000
Click 740, 160, left ;- 1 de3ia - aristera , 2 pano kato (+number pros ta kato) | back to menu
;Click 892, 160, left ;- 1 de3ia - aristera , 2 pano kato (+number pros ta kato) | back to menu NumPorte
sleep 3000
xpos += 247
Mousemove, %xpos%, %ypos%
Sleep 10
Click
Sleep 2000
Click 41, 321 ;Click in part
return
}
ResetPos()
{
Sleep 3000
Click 740, 160, left ;- 1 de3ia - aristera , 2 pano kato  | back to menu - Normal
;Click 892, 160, left ;- 1 de3ia - aristera , 2 pano kato | back to menu - NumPorte
sleep 3000
ypos += 58
xpos -= 495
Mousemove, %xpos%, %ypos%
Sleep 10
Click
Sleep 2000
Click 41, 321 ;Click in part
return
}



;--- Image capture + Tittle selection + Renaming image and Save
LoopItems(Folder,NameCheck,NumRepeat){
i=1
Loop
{
Sleep 3000
;--- Zoom + Delays
While Loopvalue<8 
{ ; Zoom in loop 
Sleep, 300
Click 41, 321
Loopvalue += 1
}
Loopvalue=0

;---Title selection

clipboard := ""
titleClipResult := ""
Mousemove 583, 222
Click, 3
Sendinput ^c
Clipwait
titleClip := clipboard
Clipwait
RegExMatch(titleClip, "\d{1,3} of \d{1,3}\s\K[^REV]*(?<!\s)", titleClipMod)
titleClipResult := RegExReplace(titleClipMod, "[\\:*?\<>|\/]", "_")

Sleep 5000 ;Delay load - Save picture

Click 284, 447 Right
Sleep 800 ;Delay for save, sometimes it clicks into google lens + sometime right click delays pop up window
Click 298, 494 Left
Sleep 1100
WinActivate , "Αποθήκευση ως"
WinGetActiveTitle, title
While % title != "Αποθήκευση ως"
{
WinActivate , "Αποθήκευση ως"
WinGetActiveTitle, title
}

;--- Renaming image + Delays
SendInput ^a
ImageName = %i% %titleClipResult%.webp
Send, % ImageName
SendInput, {NumpadEnter}
fileCheckDownload = C:\Users\user\Pictures\Screenshots\%ImageName%
Sleep 500 ; Sleep for less resource used

; https://www.autohotkey.com/docs/v1/lib/FileGetSize.htm Add check for file corrupts
; https://www.autohotkey.com/boards/viewtopic.php?t=5597
;FileGetSize, OutputVar1 , %FilePath_File%, k
;Sleep 2000
;FileGetSize, OutputVar2 , %FilePath_File%, k
;	If (OutputVar1 = OutputVar2) {
;	;File hasn't changed size in 2 seconds, must be done being constructed
;	FileMove, %FilePath_File%, %DestPattern%
;	}

Loop ; Loop file check so FileMove can work
If FileExist(fileCheckDownload)
{
FolderSetting(Folder,NameCheck,ImageName) ; Folder Settings
break
}
else
{
Sleep 500
continue
}
Click, 1914, 555
;--- Loop
i += 1
if i>%NumRepeat%
break
}
return
}


;--- Folder settings ---
FolderSetting(Folder,SubFolder,ImageName){
NameOfFile = C:\Users\user\Pictures\Screenshots\%ImageName%
NameOfFolder = %Folder%\%SubFolder%
FileMove, % NameOfFile, % NameOfFolder, 1
movedToFileCheck = %NameOfFolder%\%ImageName%
If FileExist(movedToFileCheck)
return
else
msgbox File didnt move
Return
}

; --- Input for categories
categoryInputMulti(ByRef Num1, ByRef Num2, ByRef Num3, ByRef Num4, ByRef Num5, ByRef Num6, ByRef Num7, ByRef Num8, ByRef Num9, ByRef Num10, ByRef Num11){
InputBox Num1, Reapeat, Number of times for anartisi, ,280 ,170 , 430, 430
InputBox Num2, Reapeat, Number of times for ama3oma, ,280 ,170 , 430, 430
InputBox Num3, Reapeat, Number of times for hlektrika, ,280 ,170 , 430, 430
InputBox Num4, Reapeat, Number of times for kinithras, ,280 ,170 , 430, 430
InputBox Num5, Reapeat, Number of times for plasio, ,280 ,170 , 430, 430
InputBox Num6, Reapeat, Number of times for rezerboyar, ,280 ,170 , 430, 430
InputBox Num7, Reapeat, Number of times for systhma pedeshs, ,280 ,170 , 430, 430
InputBox Num8, Reapeat, Number of times for systhma 4y3hs, ,280 ,170 , 430, 430
InputBox Num9, Reapeat, Number of times for timoni, ,280 ,170 , 430, 430
InputBox Num10, Reapeat, Number of times for troxoi, ,280 ,170 , 430, 430
InputBox Num11, Reapeat, Number of times for fota empros - organa, ,280 ,170 , 430, 430
return 
}
; [2 part]
categoryInputBy2(ByRef Num1, ByRef Num2){
InputBox Num1, Reapeat, Number of times for kinithras, ,280 ,170 , 430, 430
InputBox Num2, Reapeat, Number of times for plasio, ,280 ,170 , 430, 430
return 
}
; 6 part [NON-M]
categoryInput3(ByRef Num1, ByRef Num2, ByRef Num3, ByRef Num4, ByRef Num5, ByRef Num6){
InputBox Num1, Reapeat, Number of times for anartisi, ,280 ,170 , 430, 430
InputBox Num2, Reapeat, Number of times for hlektrika, ,280 ,170 , 430, 430
InputBox Num3, Reapeat, Number of times for kinithras, ,280 ,170 , 430, 430
InputBox Num4, Reapeat, Number of times for plasio, ,280 ,170 , 430, 430
InputBox Num5, Reapeat, Number of times for systhma pedeshs, ,280 ,170 , 430, 430
InputBox Num6, Reapeat, Number of times for timoni, ,280 ,170 , 430, 430
return 
}

; 7 part [ -7 Num porte]
categoryInputPorter4(ByRef Num1, ByRef Num2, ByRef Num3, ByRef Num4, ByRef Num5, ByRef Num6, ByRef Num7, ByRef Num8, ByRef Num9, ByRef Num10, ByRef Num11, ByRef Num12){
InputBox Num1, Reapeat, Number of times for kinithras, ,280 ,170 , 430, 430
InputBox Num2, Reapeat, Number of times for kibotio, ,280 ,170 , 430, 430
InputBox Num3, Reapeat, Number of times for plasio, ,280 ,170 , 430, 430
InputBox Num4, Reapeat, Number of times for plasio ama3, ,280 ,170 , 430, 430
InputBox Num5, Reapeat, Number of times for plasio - plast, ,280 ,170 , 430, 430
InputBox Num6, Reapeat, Number of times for plasio systh, ,280 ,170 , 430, 430
InputBox Num7, Reapeat, Number of times for esoterika e3a, ,280 ,170 , 430, 430
InputBox Num8, Reapeat, Number of times for sygkrothma sys, ,280 ,170 , 430, 430
InputBox Num9, Reapeat, Number of times for sys pedeshs, ,280 ,170 , 430, 430
InputBox Num10, Reapeat, Number of times for hlektrika egk, ,280 ,170 , 430, 430
InputBox Num11, Reapeat, Number of times for egkatastash LPG, ,280 ,170 , 430, 430
InputBox Num12, Reapeat, Number of times for egkatastash CNG, ,280 ,170 , 430, 430
return 
}

; 7 part [ Num porte]
categoryInputPorter5(ByRef Num1, ByRef Num2, ByRef Num3, ByRef Num4, ByRef Num5, ByRef Num6, ByRef Num7, ByRef Num8, ByRef Num9, ByRef Num10, ByRef Num11, ByRef Num12, ByRef Num13){
InputBox Num1, Reapeat, Number of times for kinithras, ,280 ,170 , 430, 430
InputBox Num2, Reapeat, Number of times for kibotio, ,280 ,170 , 430, 430
InputBox Num3, Reapeat, Number of times for plasio, ,280 ,170 , 430, 430
InputBox Num4, Reapeat, Number of times for plasio ama3, ,280 ,170 , 430, 430
InputBox Num5, Reapeat, Number of times for plasio - plast, ,280 ,170 , 430, 430
InputBox Num6, Reapeat, Number of times for plasio systh, ,280 ,170 , 430, 430
InputBox Num7, Reapeat, Number of times for esoterika e3a, ,280 ,170 , 430, 430
InputBox Num8, Reapeat, Number of times for sygkrothma sys, ,280 ,170 , 430, 430
InputBox Num9, Reapeat, Number of times for sys pedeshs, ,280 ,170 , 430, 430
InputBox Num10, Reapeat, Number of times for hlektrika egk, ,280 ,170 , 430, 430
InputBox Num11, Reapeat, Number of times for egkatastash LPG, ,280 ,170 , 430, 430
InputBox Num12, Reapeat, Number of times for egkatastash CNG, ,280 ,170 , 430, 430
InputBox Num13, Reapeat, Number of times for egkatastash CNG, ,280 ,170 , 430, 430
return 
}

;--- Name categories ---
categoryName(ByRef name0, ByRef name1, ByRef name2, ByRef name3, ByRef name4, ByRef name5, ByRef name6){
name0 = Maintenance
name1 = Αναρτήσεις - Τροχοί
name2 = Ηλεκτρική εγκατάσταση
name3 = Κινητήρας
name4 = Πλαίσιο - Πλαστικά μέρη - Αμαξώματα
name5 = Σύστημα πέδησης - Μετάδοσης
name6 = Τιμόνι -Σύστημα διεύθυνσης
return
}



;--- User Input + Menu Positioning and movement ---
StartMouse(){
BlockInput, MouseMoveOff
Inputbox InputMoving, maintenance, press 0 | Single_Entry  `npress 1 | NON-M  `npress 2 | Maintenance `npress 4 | NON-M Multipart `npress 5 | M Multipart `npress 6 | two category `npress 7 | numPorte -7th  , ,240 ,360 , 430, 430
FileSelectFolder, Folder, C:\Users\user\Pictures\Screenshots, 3
BlockInput, MouseMove
; naming_array := []
; num_array := []

if (InputMoving = 1){
categoryInput3(Num1,Num2,Num3,Num4,Num5,Num6)
categoryName(name0,name1,name2,name3,name4,name5,name6)
ImageSearch, xpos, ypos, 0,0,A_ScreenWidth, A_ScreenHeight, C:\Users\user\Pictures\Screenshots\ImgSearchTest\6 category\kin19.png
ypos += 20
xpos -= 550
Click, %xpos%, %ypos%
Sleep 4000
Click 41, 321 ;Click in part


LoopItems(Folder, name1, Num1)
MovingRight()
LoopItems(Folder, name2, Num2)
MovingRight()
LoopItems(Folder, name3, Num3)
ResetPos()
LoopItems(Folder, name4, Num4)
MovingRight()
LoopItems(Folder, name5, Num5)
MovingRight()
LoopItems(Folder, name6, Num6)


} else if (InputMoving = 2) {
InputBox Num0, Reapeat, Number of times for maintenance, ,280 ,170 , 430, 430
categoryInput3(Num1,Num2,Num3,Num4,Num5,Num6)
categoryName(name0,name1,name2,name3,name4,name5,name6)
ImageSearch, xpos, ypos, 0,0,A_ScreenWidth, A_ScreenHeight, C:\Users\user\Pictures\Screenshots\ImgSearchTest\6 category\hlektrika.png
; err := ErrorLevel
; MsgBox, 64, ErrorLevel, %err%
ypos += 5
xpos -= 410
Click, %xpos%, %ypos%

; Image search for button "maintenance" + move

Sleep 2000
Click 41, 321 ;Click in part
LoopItems(Folder, name0, Num0)
MovingRight()
LoopItems(Folder, name1, Num1)
MovingRight()
LoopItems(Folder, name2, Num2)
ResetPos()
LoopItems(Folder, name3, Num3)
MovingRight()
LoopItems(Folder, name4, Num4)
MovingRight()
LoopItems(Folder, name5, Num5)
ResetPos()
LoopItems(Folder, name6, Num6)


} else if (InputMoving = 4) {
categoryName(name0,name1,name2,name3,name4,name5,name6)
categoryInputMulti(Num1,Num2,Num3,Num4,Num5,Num6,Num7,Num8,Num9,Num10,Num11)
ImageSearch, xpos, ypos, 0,0,A_ScreenWidth, A_ScreenHeight, C:\Users\user\Pictures\Screenshots\ImgSearchTest\rez.png

ypos -= 45
xpos -= 460
Click, %xpos%, %ypos%
Sleep 2000
Click 41, 321 ;Click in part

LoopItems(Folder, name1, Num1)
MovingRight()
LoopItems(Folder, name4, Num2)
MovingRight()
LoopItems(Folder, name2, Num3)
ResetPos()
LoopItems(Folder, name3, Num4)
MovingRight()
LoopItems(Folder, name4, Num5)
MovingRight()
LoopItems(Folder, name4, Num6)
ResetPos()
LoopItems(Folder, name5, Num7)
MovingRight()
LoopItems(Folder, name3, Num8)
MovingRight()
LoopItems(Folder, name6, Num9)
ResetPos()
LoopItems(Folder, name1, Num10)
MovingRight()
LoopItems(Folder, name2, Num11)


} else if (InputMoving = 5) {
categoryName(name0,name1,name2,name3,name4,name5,name6)
InputBox Num0, Reapeat, Number of times for maintenance
categoryInputMulti(Num1,Num2,Num3,Num4,Num5,Num6,Num7,Num8,Num9,Num10,Num11)
ImageSearch, xpos, ypos, 0,0,A_ScreenWidth, A_ScreenHeight, C:\Users\user\Pictures\Screenshots\ImgSearchTest\ama3oma.png
ypos -= 5
xpos -= 440
Click, %xpos%, %ypos%
Sleep 2000
Click 41, 321 ;Click in part


LoopItems(Folder, name0, Num0)
MovingRight()
LoopItems(Folder, name1, Num1)
MovingRight()
LoopItems(Folder, name4, Num2)
ResetPos()
LoopItems(Folder, name2, Num3)
MovingRight()
LoopItems(Folder, name3, Num4)
MovingRight()
LoopItems(Folder, name4, Num5)
ResetPos()
LoopItems(Folder, name4, Num6)
MovingRight()
LoopItems(Folder, name5, Num7)
MovingRight()
LoopItems(Folder, name3, Num8)
MovingRight()
LoopItems(Folder, name6, Num9)
ResetPos()
LoopItems(Folder, name1, Num10)
MovingRight()
LoopItems(Folder, name2, Num11)

} else if (InputMoving = 6){
categoryName(name0,name1,name2,name3,name4,name5,name6) ; Only use 3 and 4, Kinitiras - plastika antistixa
categoryInputBy2(Num1,Num2)
ImageSearch, xpos, ypos, 0,0,A_ScreenWidth, A_ScreenHeight, C:\Users\user\Pictures\Screenshots\ImgSearchTest\empty2.png
ypos += 65
xpos -= 500
Click, %xpos%, %ypos%
Sleep 2000
Click 41, 321 ;Click in part
LoopItems(Folder, name3, Num1)
MovingRight()
LoopItems(Folder, name4, Num2)

}else if (InputMoving = 0){
categoryName(name0,name1,name2,name3,name4,name5,name6) 
InputBox Num0, Reapeat, Number of times for maintenance
Click 1
Sleep 2000
Click 41, 321 ;Click in part
LoopItems(Folder, name0, Num0)

}
else if (InputMoving = 7) {
categoryName(name0,name1,name2,name3,name4,name5,name6)
categoryInputPorter4(Num1,Num2,Num3,Num4,Num5,Num6,Num7,Num8,Num9,Num10,Num11,Num12)
ImageSearch, xpos, ypos, 0,0,A_ScreenWidth, A_ScreenHeight, C:\Users\user\Pictures\Screenshots\ImgSearchTest\NumPorte.png

ypos -= 5
xpos -= 460
Click, %xpos%, %ypos%
Sleep 2000
Click 41, 321 ;Click in part

LoopItems(Folder, name3, Num1)
MovingRight()
LoopItems(Folder, name3, Num2)
MovingRight()
LoopItems(Folder, name5, Num3)
ResetPos()
LoopItems(Folder, name4, Num4)
MovingRight()
LoopItems(Folder, name4, Num5)
MovingRight()
LoopItems(Folder, name0, Num6) ; Split images correctly by hand
ResetPos()
LoopItems(Folder, name4, Num7) 
MovingRight()
LoopItems(Folder, name1, Num8) ; 2 akyra, timoni , plastika
MovingRight()
LoopItems(Folder, name5, Num9)
ResetPos()
LoopItems(Folder, name2, Num10)
MovingRight()
LoopItems(Folder, name4, Num11)
MovingRight()
LoopItems(Folder, name4, Num12)

}
else if (InputMoving = 8) {
categoryName(name0,name1,name2,name3,name4,name5,name6)
categoryInputPorter5(Num1,Num2,Num3,Num4,Num5,Num6,Num7,Num8,Num9,Num10,Num11,Num12,Num13)
ImageSearch, xpos, ypos, 0,0,A_ScreenWidth, A_ScreenHeight, C:\Users\user\Pictures\Screenshots\ImgSearchTest\NumPorte.png

ypos -= 5
xpos -= 460
Click, %xpos%, %ypos%
Sleep 2000
Click 41, 321 ;Click in part

LoopItems(Folder, name3, Num1)
MovingRight()
LoopItems(Folder, name3, Num2)
MovingRight()
LoopItems(Folder, name5, Num3)
ResetPos()
LoopItems(Folder, name4, Num4)
MovingRight()
LoopItems(Folder, name4, Num5)
MovingRight()
LoopItems(Folder, name0, Num6) ; Split images correctly by hand
ResetPos()
LoopItems(Folder, name4, Num7) 
MovingRight()
LoopItems(Folder, name4, Num8) 
MovingRight()
LoopItems(Folder, name1, Num9) ; 2 akyra, timoni , plastika
ResetPos()
LoopItems(Folder, name5, Num10)
MovingRight()
LoopItems(Folder, name2, Num11)
MovingRight()
LoopItems(Folder, name4, Num12)
ResetPos()
LoopItems(Folder, name4, Num13)

}

else {
ExitApp
}

return
}



;=== Pasting Scooter Name in input form ===
#IfWinActive ahk_class Chrome_WidgetWin_1
NumpadAdd::
Sendinput ^v
saveClip := ""
saveClip := clipboard
SendInput {Tab}
Sleep 1
SendInput {NumpadEnter}
Sleep 1
;------------------------------------------|
;                                          |
clipboard = Ape Classic 400 E4 2017-2023 - Ape Classic 400 E4 VAN 2019-2023 ; |
;                                          |
;------------------------------------------|
ClipWait
sleep 100
SendInput ^v 
Sleep 1100
SendInput {NumpadEnter}
;SendInput {Tab}
;SendInput {Tab}
;SendInput {Tab}
;SendInput {Tab}
;SendInput {Tab}
clipboard := % saveClip
ClipWait
#IfWinActive
return



;=== Start Sequence ===

^Numpad0::
Coordmode, Mouse, Relative
SendMode Input
BlockInput, MouseMove
xpos := ypos := 0
global xpos,ypos
Click
BrowserBack()
StartMouse()
Click 722, 160, left ;- 1 de3ia - aristera , 2 pano kato (+number pros ta kato) | back to menu
BlockInput, MouseMoveOff
msgbox, 4096, , Done!

return
