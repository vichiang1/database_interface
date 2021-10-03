// # Copyright 2021 Vitalant
// # Author: Vincent Chiang
// #
// # This program is free software: you can redistribute it and/or modify
// # it under the terms of the GNU Affero General Public License as published by
// # the Free Software Foundation, either version 3 of the License, or
// # (at your option) any later version.
// #
// # The software is distributed in the hope that it will be useful,
// # but WITHOUT ANY WARRANTY; without even the implied warranty of
// # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// # GNU Affero General Public License for more details.
// #
// # You should have received a copy of the GNU Affero General Public License
// # along with this software. If not, see <http://www.gnu.org/licenses/>. 
$(document).ready(function () {
    $("select").multiselect({
      buttonWidth: '140px',
      numberDisplayed: 1,
      includeSelectAllOption: false,
    });
    $("select").multiselect('updateButtonText');
  });

// var expanded = false;

// function showCheckboxes() {
//   var checkboxes = document.getElementById("checkboxes");
//   if (!expanded) {
//     checkboxes.style.display = "block";
//     expanded = true;
//   } else {
//     checkboxes.style.display = "none";
//     expanded = false;
//   }
// }

