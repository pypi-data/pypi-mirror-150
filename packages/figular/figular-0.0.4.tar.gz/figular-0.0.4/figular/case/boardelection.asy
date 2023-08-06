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

import "concept/circle.asy" as circle;
import "org/orgchart.asy" as orgchart;
import "figular/cleanse.asy" as cleanse;
import "figular/defpicture.asy" as defpicture;

struct boardelection {

  pen ourblack = gray(0.2);
  pen ourwhite = rgb(0.9, 0.9, 0.9);
  pen ourgreen = rgb("3da639");

  defpicture defpicture;
  circle circle1;
  circle circle2;
  orgchart orgchart; 
  string title;
  string subtitle;

  string circle1lines[];
  string circle1title;
  string circle1subtitle;
  string circle2lines[];
  string orglines[];

  defpicture dopie(real scaling, int percent, pen ourwhite) {
    defpicture defpic;
    real scalingadjust = 0.55;
    if(percent < 100) {
      path pie = (0, 0) -- arc((0,0), 1, 90, 90-360*(percent/100), direction=CW) -- cycle;
      pie = scale(scaling*scalingadjust)*pie;
      defpic.push(
        drawnpath(pie,
                  new void(picture pic, path p) { fill(pic, p, ourwhite); })
        );
      defpic.push(
        drawnpath(scale(scaling*scalingadjust)*unitcircle,
                  new void(picture pic, path p) { draw(pic, p, ourwhite); })
        );
    } else {
      defpic.push(
        drawnpath(scale(scaling*scalingadjust)*unitcircle,
                  new void(picture pic, path p) { fill(pic, p, ourwhite); })
        );
    }
    return defpic;
  }

  defpicture mydrawcard(string title, string subtitle) {
    defpicture defpic;
    int fontsize = 12;
    real corner_dia = 3 * fontsize ;
    real card_height = 2.5 * corner_dia ;
    real card_width = 5 * corner_dia;
    pen titlepen = fontsize(fontsize) + AvantGarde("b");
    pen subtitlepen = fontsize(9) + Helvetica();

    // Box
    defpic.push(
      drawnpath((-card_width/2,-card_height/2 + corner_dia/2)--
                (-card_width/2,card_height/2 - corner_dia/2){up}..
                (-card_width/2+corner_dia/2,card_height/2)--
                (card_width/2-corner_dia/2,card_height/2){right}..
                (card_width/2,card_height/2 - corner_dia/2)--
                (card_width/2,-card_height/2 + corner_dia/2){down}..
                (card_width/2-corner_dia/2,-card_height/2)--
                (-card_width/2+corner_dia/2,-card_height/2){left}..
                cycle,
      new void(picture pic, path p) { fill(pic, p, ourblack); })
      );

    // Title
    // As we are using align=N we add the equivalent of baseline() to the END of
    // our title to ensure its final line is always the typeface's full height
    // thus allowing us to position it the same regardless of the presence of
    // descenders
    string tex_strut = "\vphantom{\strut}"; 
    string minipagespec = title + tex_strut;
    // This is a rule of thumb that works for us
    real descenderadjust = fontsize/2;
    real titleoffset = .2*corner_dia;
    defpic.push(
      Label(minipage(minipagespec, width=2.5*corner_dia),
            (corner_dia*3/4, titleoffset - descenderadjust), N, titlepen+ourwhite)
      );

    // Big underline
    defpic.push(
      drawnpath((-corner_dia/2,0)--(2*corner_dia,0),
      new void(picture pic, path p) { draw(pic, p, linewidth(1)+ourwhite); })
      );

    // Subtitle
    // Similar to title but add the baseline strut to the start as align=S.
    string role = subtitle;
    string[] info = split(subtitle, ",");
    if(info.length == 3) {
      role = info[0];
      int pcent = round((int)info[1] / (int)info[2] * 100);
      string piecaption = (string)info[1] + " of " + (string)info[2] + " month term served";
      defpic.push(dopie(corner_dia, pcent, ourwhite), (-1.5*corner_dia, titleoffset + fontsize*3/4));
      minipagespec = "\centering{" + piecaption + "}" ;
      defpic.push(
        Label(minipage(minipagespec, width=1.75*corner_dia),(-1.5*corner_dia,-titleoffset),
              S, subtitlepen+ourwhite)
        );
    }

    minipagespec = baseline(role);
    defpic.push(
      Label(minipage(minipagespec, width=2.5*corner_dia),(corner_dia*3/4,-titleoffset),
            S, subtitlepen+ourwhite)
      );

    return defpic;
  }

  void drawcircle(circle circle, string title, string subtitle, pair pos) {
    circle.draw();
    for(drawnpath dp: circle.defpicture.drawnpaths) {
      pair centre = (min(dp.p) + (max(dp.p)-min(dp.p))/2);
      defpicture.push(
        drawnpath(shift(pos)*((0,0) -- centre),
        new void(picture pic, path p) { draw(pic, p, p=ourgreen); })
        );
    }

    if(title != "" || subtitle != "") {
      defpicture.push(
        drawnpath(shift(pos)*circle((0,0), size(circle.defpicture).x/5),
        new void(picture pic, path p) { fill(pic, p, p=white); })
        );

      string minipagespec;
      real tightwidth = size(circle.defpicture).x/2;

      if(title != "") {
        minipagespec = "\centering{" + title + "}";
        Label titlelabel = Label(minipage(minipagespec, width=tightwidth),
                                 pos, align=N, fontsize(36) + Helvetica() + ourgreen);
        path[] titlepaths = texpath(titlelabel);
        defpicture.push(titlelabel);
        // Adjust width for subtitle to be tight to title
        tightwidth = max(titlepaths).x-min(titlepaths).x;
      }
      if(subtitle != "") {
        minipagespec = "\centering{" + subtitle + "}";
        defpicture.push(Label(minipage(minipagespec, width=tightwidth),
                              shift(pos)*(0, -lineskip()), align=S, fontsize(16) + Helvetica() + ourblack));
      }
    }

    defpicture.push(circle.defpicture, pos);
  }

  struct circlesetup {
    string[] lines;
    string title;
    string subtitle;
  }

  circlesetup circle1setup, circle2setup;

  typedef void inputstrategy(string);

  void inputorgchart(string arg) {
    orglines.push(arg);
  }

  void inputtitles(string arg) {
    if(substr(arg, 0, 3) == "## ") {
      subtitle = cleanse.escape(substr(arg, 3));
    } else if(substr(arg, 0, 2) == "# ") {
      title = cleanse.escape(substr(arg, 2));
    }
  }

  inputstrategy inputcircle(circlesetup circlesetup) {
    circlesetup.lines.push("minRadius=250");

    return new void(string arg) {
      if(substr(arg, 0, 3) == "## ") {
        circlesetup.subtitle = cleanse.escape(substr(arg, 3));
      } else if(substr(arg, 0, 2) == "# ") {
        circlesetup.title = cleanse.escape(substr(arg, 2));
      } else {
        circlesetup.lines.push("blob="+arg);
      }
    } ;
  }

  void operator init(string[] input) {
    inputstrategy[] strats = new inputstrategy[]{ inputorgchart,
                                                  inputcircle(circle2setup),
                                                  inputcircle(circle1setup),
                                                  inputtitles };
    inputstrategy currentstrat = strats.pop();

    for(string arg: input) {
      if(arg == "---") {
        currentstrat = strats.pop();
      } else {
        currentstrat(arg);
      }
    }

    solvepairmax solver = solvepairmax(2);
    circle1 = circle(circle1setup.lines);
    circle1.solveblobsize(solver);
    circle2 = circle(circle2setup.lines);
    circle2.solveblobsize(solver);
    orgchart = orgchart(orglines);
  }

  void draw() {
    orgchart.drawer = mydrawcard;
    orgchart.draw();

    // This is horrible manipulation but it'll do for now
    orgchart.defpic.drawnpaths.delete();
    if(orgchart.defpic.defpicturepos.length > 1) {
      orgchart.defpic.defpicturepos.delete(orgchart.defpic.defpicturepos.length-1);
    }
    defpicture.push(orgchart.defpic, (0, 0));

    drawcircle(circle1, circle1setup.title, circle1setup.subtitle,
               (-700, -size(orgchart.defpic).y/2));
    drawcircle(circle2, circle2setup.title, circle2setup.subtitle,
               (700, -size(orgchart.defpic).y/2));

    pair titlemiddle = (0, 100);
    defpicture.push(Label(title, titlemiddle, align=N, fontsize(144) + AvantGarde("b") + ourblack));
    defpicture.push(Label(subtitle, shift(0, -lineskip(fontsize(144/2)))*titlemiddle, align=N, fontsize(144/2) + AvantGarde("b") + ourgreen));
  }

  void draw(picture pic) {
    if(defpicture.empty()) {
      draw();
    }
    defpicture.draw(pic);
  }
}

void run(picture pic, string[] input) {
  boardelection be = boardelection(input);
  be.draw(pic);
}
