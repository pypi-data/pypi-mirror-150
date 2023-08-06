// SPDX-FileCopyrightText: 2021-2 Galagic Limited, et. al. <https://galagic.com>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
//
// figular generates visualisations from flexible, reusable parts
//
// For full copyright information see the AUTHORS file at the top-level
// directory of this distribution or at
// [AUTHORS](https://gitlab.com/thegalagic/figular/AUTHORS.md)
//
// This program is free software: you can redistribute it and/or modify it under
// the terms of the GNU Affero General Public License as published by the Free
// Software Foundation, either version 3 of the License, or (at your option) any
// later version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
// details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.

import "figular/cleanse.asy" as cleanse;
import "figular/defpicture.asy" as defpicture;
import "figular/paramsolver.asy" as paramsolver;
import "figular/stylereset.asy" as stylereset;

struct circle {
  defpicture defpicture;
  string[] blobs={};
  real degreeStart=0;
  bool middle=false;
  string font = "cmr";
  parampair blobsizeparam;

  private pair getlabelsize(string text, string font) {
    picture pic;
    label(pic, text, font("OT1", font, "m", "n"));
    return size(pic);
  }

  private pair getmaxlabelsize() {
    pair maxlabelsize = (0,0);
    for(string blobName : blobs) {
      pair size = getlabelsize(blobName, font);
      if (size.x > maxlabelsize.x) {
        maxlabelsize = (size.x, maxlabelsize.y);
      }
      if (size.y > maxlabelsize.y) {
        maxlabelsize = (maxlabelsize.x, size.y);
      }
    }
    return maxlabelsize;
  }

  private void drawblob(pair pos, string blobName, real blobradius, string font) {
    defpicture.push(
      drawnpath(circle(pos, blobradius),
      new void(picture pic, path p) { fill(pic, p, p=gray(0.2)); })
      );
    defpicture.push(
      Label(blobName, pos, p=font("OT1", font, "m", "n") + rgb(0.9,0.9,0.9))
      );
  }

  private void drawcircle(string[] blobNames, real degreeStart=0,
                   bool middle=false, string font) {
    real magicnumber = 10;
    pair maxlabelsize = this.blobsizeparam.get();
    real blobradius = max(maxlabelsize.x, maxlabelsize.y)/2 + magicnumber;

    if(middle && blobNames.length > 1) {
      drawblob((0,0), blobNames[0], blobradius, font);
      blobNames.delete(0,0);
    }

    real degreeStep = 360 / blobNames.length;
    real radius = 0;

    radius = blobradius + magicnumber;
    if (blobNames.length > 1) {
        radius = (blobradius + magicnumber) / Sin(degreeStep/2);
    }

    if(middle && radius < (2*blobradius)) {
      //There's a chance radius is too small to make space for middle blob
      radius = 2*blobradius + (magicnumber * 2);
    }

    pair pos = rotate(-degreeStart) * (0, radius);

    for(string blobName : blobNames) {
      drawblob(pos, blobName, blobradius, font);
      pos = rotate(-degreeStep) * pos;
    }
  }

  void operator init(string[] input) {
    string arg;
    string[] parts;

    for(string arg: input) {
      parts = split(arg, "=");

      if(parts[0] == "blob" && parts.length > 1) {
        string cleansed = cleanse.escape(substr(arg, 5));
        if(length(cleansed) > 0) {
          blobs.push(cleansed);
        }
      } else if(parts[0] == "degreeStart" && parts.length > 1) {
        degreeStart = (real)parts[1];
      } else if(parts[0] == "middle" && parts.length > 1) {
        middle = parts[1] == "true";
      } else if(parts[0] == "font" && parts.length > 1) {
        font = parts[1];
      }
    }

    this.blobsizeparam = parampair(getmaxlabelsize);
  }

  void draw() {
    if(blobs.length != 0) {
      drawcircle(blobs, degreeStart, middle, font);
    }
  }

  void draw(picture pic) {
    if(defpicture.empty()) {
      draw();
    }
    defpicture.draw(pic);
  }

  void solveblobsize(solvepair solver) {
     solver.suggest(this.blobsizeparam);
  }

}

void run(picture pic, string[] input) {
  circle circle = circle(input);
  circle.draw(pic);
}
