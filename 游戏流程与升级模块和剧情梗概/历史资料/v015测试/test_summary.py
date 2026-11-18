# coding: utf-8
from pathlib import Path
import shutil, subprocess, tempfile
source=(Path(__file__).resolve().parents[1]/'index.html').read_text().split('<script>')[1].split('</script>')[0]
prefix='var navigator={language:"zh"};var document={documentElement:{},getElementById:function(){return {}}};var localStorage={getItem:function(){return null},setItem:function(){}};var performance={now:function(){return 0}};\n'
test="""render=()=>{};toast=()=>{};save=()=>{};function check(v,m){if(!v)throw Error(m)}
s=fresh();s.mode='summary';s.savedAt=1000;s.thoughts=200;s.disturbances=50;s.worldview='magic';s.species='plant';s.raceResources={mana:150};s.echo=3;check(settleOffline(361000)===null,'summary does not report offline');check(s.thoughts===200&&s.disturbances===50&&s.raceResources.mana===150,'summary resources do not grow');check(s.savedAt===361000,'summary timestamp advances');buyStageChoice('mindStorage');check(s.legacyStorage.mind===1&&s.echo===1,'echo purchases permanent upgrade');check(s.thoughts===200&&s.raceResources.mana===150,'legacy purchase does not spend run resources');
s.mode='growth';s.savedAt=1000;s.runThoughts=0;s.thoughts=0;s.disturbances=0;check(settleOffline(11000).used===10,'active run offline remains enabled');
print('summary offline suppression, frozen stocks and permanent legacy purchase OK');return;\n"""
source=source.replace("  $('closeOffline').addEventListener('click'",test+"  $('closeOffline').addEventListener('click'",1)
jsc=shutil.which('jsc') or '/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
with tempfile.TemporaryDirectory() as folder:
    script=Path(folder)/'summary.js';script.write_text(prefix+source);subprocess.run([jsc,str(script)],check=True)
