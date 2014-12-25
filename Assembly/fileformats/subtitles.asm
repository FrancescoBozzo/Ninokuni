;;----------------------------------------------------------------------------;;
;;  Add a second text line (replace subtitle command separator 0xA to 0x3)
;;  Copyright 2014 Benito Palacios (aka pleonex)
;;
;;  Licensed under the Apache License, Version 2.0 (the "License");
;;  you may not use this file except in compliance with the License.
;;  You may obtain a copy of the License at
;;
;;      http://www.apache.org/licenses/LICENSE-2.0
;;
;;  Unless required by applicable law or agreed to in writing, software
;;  distributed under the License is distributed on an "AS IS" BASIS,
;;  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
;;  See the License for the specific language governing permissions and
;;  limitations under the License.
;;----------------------------------------------------------------------------;;

@SPLITTER equ #0x03

.thumb
.org 02137F04h
    CMP     R3, @SPLITTER

.org 02137F24h
    CMP     R0, @SPLITTER
