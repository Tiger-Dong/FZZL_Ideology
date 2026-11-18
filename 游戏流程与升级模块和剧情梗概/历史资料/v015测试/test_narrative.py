# coding: utf-8
from pathlib import Path
import shutil, subprocess, tempfile
source=(Path(__file__).resolve().parents[1]/'index.html').read_text().split('<script>')[1].split('</script>')[0]
prefix='var navigator={language:"zh"};var document={documentElement:{},getElementById:function(){return {}}};var localStorage={getItem:function(){return null},setItem:function(){}};var performance={now:function(){return 0}};\n'
test='''render=()=>{};toast=()=>{};save=()=>{};function check(v,m){if(!v)throw Error(m)}
for(const species of ['human','animal','plant']){s=fresh();s.mode='world';s.species=species;s.worldview='magic';s.runThoughts=1000;s.network=true;s.raceResources={mana:100};let beat=stageNarrative();check(beat[0]==='灾难预兆'&&!/倒下|截断|失去载体/.test(beat[1]),species+' early');prepareCrisis('protect');beat=stageNarrative();check(beat[0]==='灾前准备'&&beat[1].includes(crisisActions()[0].name),species+' prepare');beginTrial();check(stageNarrative()[0]==='应对选择'&&s.log[0].text.includes('开始考虑'),species+' choice');s.mode='world';check(stageNarrative()[0]==='灾前准备'&&!s.crisisResult,species+' cancel');beginTrial();resolveTrial('resources');check(s.mode==='summary'&&s.lastTrial.includes('未能存活')&&s.lastTrial.includes('载体'),species+' failed ending');}
for(const species of ['human','animal','plant']){s=fresh();s.mode='world';s.species=species;s.worldview='magic';s.runThoughts=1000;s.network=true;s.raceResources={mana:100};const i={human:0,animal:1,plant:0}[species];s.raceUpgrades[`race-magic-${species}-${i}`]=1;prepareCrisis('protect');beginTrial();resolveTrial('resources');check(s.mode==='aftermath'&&stageNarrative()[0]==='灾难结果',species+' result');s.mode='world';check(stageNarrative()[0]==='灾后成长'&&!stageNarrative()[1].includes('失去了载体'),species+' alive');finishSurvivedCycle();check(s.mode==='summary'&&s.lastTrial.includes('危机过后')&&s.lastTrial.includes('最终'),species+' ending');}
print('narrative states, cancel, failure and survivor endings OK');return;\n'''
source=source.replace("  $('closeOffline').addEventListener('click'",test+"  $('closeOffline').addEventListener('click'",1)
jsc=shutil.which('jsc') or '/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
with tempfile.TemporaryDirectory() as folder:
 script=Path(folder)/'narrative.js';script.write_text(prefix+source);subprocess.run([jsc,str(script)],check=True)
