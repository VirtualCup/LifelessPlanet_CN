from UnityText import UnityText;
from UnityUIfont import UnityUIfont;
from StringHelper import StringHelper;
from xml.dom.minidom import parseString;
from PIL import Image;
import csv;
import sys;
import os;
import shutil;

reload(sys);
sys.setdefaultencoding('utf8');

def save_to_csv():
	utxt_1 = UnityText("OriginalFile/unnamed asset-resources.assets-24.dat");
	utxt_2 = UnityText("OriginalFile/unnamed asset-resources.assets-31.dat");
	utxt_3 = UnityText("OriginalFile/unnamed asset-resources.assets-48.dat");
	utxt_4 = UnityText("OriginalFile/unnamed asset-resources.assets-58.dat");
	utxt_5 = UnityText("OriginalFile/unnamed asset-resources.assets-60.dat");
	utxt_6 = UnityText("OriginalFile/unnamed asset-resources.assets-68.dat");

	f = open("localization.csv", "wb");
	csv_writer = csv.writer(f);
	
	utxts = [utxt_1, utxt_2, utxt_3, utxt_4, utxt_5, utxt_6];
	for utxt in utxts:
		udom = parseString(utxt.get_txt());
		rows = udom.documentElement.getElementsByTagName("entry");
		for row in rows:
			id = row.getAttribute("name");
			lang = row.childNodes[0].data;
			csv_writer.writerow([lang, "", id, utxt.name]);
	
	f.close();

def csv_to_raw():	
	f = open("localization.new.csv", "rb");
	csv_reader = csv.reader(f);
	dits = {};
	for csv_row in csv_reader:
		utxt_name = csv_row[3];
		id = csv_row[2];
		lang = csv_row[1];
		if not dits.has_key(utxt_name):
			dits[utxt_name] = {};
		dits[utxt_name][id] = lang;
	f.close();
	
	ufile_ids = ["24", "31", "48", "58", "60", "68"];
	us = [];
	for ufile_id in ufile_ids:
		utxt = UnityText("OriginalFile/unnamed asset-resources.assets-{0}.dat".format(ufile_id));
		udom = parseString(utxt.get_txt());
		us.append([udom, utxt, ufile_id]);

	for u in us:
		udom = u[0];
		utxt = u[1];
		ufile_id = u[2];
		elms = udom.documentElement.getElementsByTagName("entry");
		for elm in elms:
			id = elm.getAttribute("name");
			elm.childNodes[0].data = dits[utxt.name][id];
		
		xmlstr = udom.toxml();
		utxt.set_txt(xmlstr[22:]);
		utxt.save_to_raw("LifelessPlanet/unnamed asset-resources.assets-{0}.dat".format(ufile_id));

def gen_font_image(bmfc_filepath, output_filepath):
	bmfont_tool_path = "E:\\BMFont\\bmfont.com";
	text_file_path = "\"Font\\textmin.txt\"";
	bmfc_filepath = "\"" + bmfc_filepath.replace("/", "\\") + "\"";
	output_filepath = "\"" + output_filepath.replace("/", "\\") + "\"";
	commandstr = " ".join((bmfont_tool_path , "-c" ,bmfc_filepath, "-o", output_filepath, "-t" ,text_file_path));
	os.system(commandstr.encode('mbcs'));
		
def gen_new_font(fnt_filepath):
	uifont = UnityUIfont("OriginalFile/unnamed asset-sharedassets0.assets-671.dat", version = 9, is_oleder_ngui_version = True);
	uifont.read_from_bmfont(fnt_filepath, fullszie = [2048, 1024], offset = [1024, 0]);
	uifont.save_to_raw("LifelessPlanet/unnamed asset-sharedassets0.assets-671.dat");
	
def combine_png(left_image_path, right_image_path, out_path):
	iml = Image.open(left_image_path);
	imr = Image.open(right_image_path);
	imo = Image.new('RGBA', (2048, 1024), 'red');
	
	imo.paste(iml.convert("RGBA").crop(), (0, 0, iml.size[0], iml.size[1]));
	imo.paste(imr.convert("RGBA").crop(), (1024, 0, 1024 + imr.size[0], imr.size[1]));
	
	imo.save(out_path);
	
sh = StringHelper();
sh.add_file_text("localization.new.csv");
sh.add_western();
f = open("Font/textmin.txt", "wb");
f.write(sh.get_chars().decode("utf-8").encode("utf-8-sig"));
f.close();
	
csv_to_raw();
gen_font_image("Font/LPHUD1-sharedassets0.assets-64.bmfc", "Font/LPHUD1-sharedassets0.assets-64.fnt");
combine_png("OriginalFile/LPHUD1-sharedassets0.assets-64.png", "Font/LPHUD1-sharedassets0.assets-64_0.png", "LifelessPlanet/LPHUD1-sharedassets0.assets-64.png");
gen_new_font("Font/LPHUD1-sharedassets0.assets-64.fnt");
