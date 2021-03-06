;;----------------------------------------------------------------------------;;
;;  Hacks for overlay 20 for arm9
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
.nds
.open overlay9_20.bin, 0x02159FE0

.relativeinclude on
.erroronwarning on

.include fileformats\spellsname\spells_ov20.asm
.include fileformats\skillsname\skills_zoom.asm
.include fileformats\familiarname\familiar_zoom.asm
.include textbox\menu_rupe.asm

.close
; EOF ;
