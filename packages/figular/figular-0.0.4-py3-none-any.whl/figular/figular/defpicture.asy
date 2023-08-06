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

struct drawnpath {
  path p;
  void drawroutine(picture, path);

  void operator init(path p, void drawroutine(picture, path)) {
    this.p = p;
    this.drawroutine = drawroutine;
  }
}

struct defpicture {
  struct defpicturepos {
    defpicture dp;
    pair pos;

    void operator init(defpicture dp, pair pos) {
      this.dp = dp; this.pos = pos;
    }
  }


  pair min, max; 
  drawnpath[] drawnpaths = new drawnpath[]{};
  Label[] labels = new Label[]{};
  defpicturepos[] defpicturepos = new defpicturepos[]{};

  private void updatebounds(pair possmin, pair possmax) {
    if(possmin.x < min.x) { min = (possmin.x, min.y); }
    if(possmin.y < min.y) { min = (min.x, possmin.y); }
    if(possmax.x > max.x) { max = (possmax.x, max.y); }
    if(possmax.y > max.y) { max = (max.x, possmax.y); }
  }

  private void updatebounds(drawnpath dp) {
    // TODO: This is naive? We take no account of pen width/fill etc.
    pair possmin, possmax;
    possmin = min(dp.p);
    possmax = max(dp.p);
    updatebounds(possmin, possmax);
  }

  private void updatebounds(defpicture dp, pair pos) {
    pair possmin, possmax;
    possmin = shift(pos)*dp.min;
    possmax = shift(pos)*dp.max;
    updatebounds(possmin, possmax);
  }

  void operator init(drawnpath[] dp, Label[] l) {
    this.drawnpaths = dp;
    this.labels = l;
  }

  void push(drawnpath dp) {
    drawnpaths.push(dp);
    updatebounds(dp);
  }

  void push(Label l) {
    labels.push(l);
    // TODO: update min, max bounds somehow with size of label
  }

  void push(defpicture dp, pair pos) {
    defpicturepos.push(defpicturepos(dp, pos));
    updatebounds(dp, pos);
  }

  bool empty() {
    return drawnpaths.length == 0 && 
           labels.length == 0 &&
           defpicturepos.length == 0;
  }

  void draw(picture pic) {
    for(drawnpath dp: drawnpaths) {
      dp.drawroutine(pic, dp.p);
    }
    for(Label lb: labels) {
      label(pic, lb);
    }
    for(defpicturepos dpp: defpicturepos) {
      picture result;
      dpp.dp.draw(result);
      add(pic, result, dpp.pos);
    }
  }
}

//
// [asymptote/plain_picture.asy at master · vectorgraphics/asymptote](https://github.com/vectorgraphics/asymptote/blob/master/base/plain_picture.asy#L1124)
//
// We really don't want to end up rewriting picture...
// or do we subclass it and replace a bunch of its methods with ours?
//
// Do we really need to support all the same methods as picture?
// It's not 100% necessary though nice for new users
//
// Nasty that we reach inside defpicture

pair size(defpicture pic) {
  return pic.max-pic.min;
}

pair min(defpicture pic) {
  return pic.min;
}

pair max(defpicture pic) {
  return pic.max;
}

void add(defpicture dest, defpicture src, pair pos) {
  dest.push(src, pos);
}
