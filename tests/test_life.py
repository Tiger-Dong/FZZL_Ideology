# coding: utf-8
from pathlib import Path
import shutil, subprocess, tempfile
source=(Path(__file__).resolve().parents[1]/'index.html').read_text().split('<script>')[1].split('</script>')[0]
prefix='var navigator={language:"zh"};var document={documentElement:{},getElementById:function(){return {}}};var localStorage={getItem:function(){return null},setItem:function(){}};var performance={now:function(){return 0}};\n'
test='''render=()=>{};toast=()=>{};save=()=>{};function check(v,m){if(!v)throw Error(m)}
for(const species of ['human','animal','plant'])for(const world of ['magic','cultivation','technology']){s=fresh();s.mode='world';s.species=species;s.worldview=world;s.runThoughts=1000;s.network=true;s.raceResources={[worlds[world].currency]:300};let def=speciesUpgradeDefs()[species==='animal'?1:0];check(!s.lifeMoments.length,'no fabricated memory');buyUpgrade(def.id);check(s.lifeMoments.length===1&&stageNarrative()[1].includes(s.lifeMoments[0].text),'growth displayed');buyUpgrade(def.id);check(s.lifeMoments.length===1,'no duplicate');prepareCrisis('protect');check(stageNarrative()[1].includes(s.lifeMoments[0].text),'visible while preparing');beginTrial();resolveTrial('resources');check(s.crisisResult.level>0,'survival');s.mode='world';finishSurvivedCycle();let h=s.cycleHistory[0];check(h.lifeMoments.length===1&&h.lifeMemory===s.lifeMoments[0].memory,'history snapshot');s.cycle=2;check(openingMemory().includes(h.lifeMemory),'next opening');}
s=fresh();s.cycle=2;s.cycleHistory=[{species:'动物',choice:'保存资源',kept:1,keepLabel:'基础资源'}];check(openingMemory().includes('动物'),'legacy fallback');
s=fresh();s.mode='world';s.species='plant';s.worldview='cultivation';s.runThoughts=1000;s.network=false;s.raceResources={qi:100};buyUpgrade(speciesUpgradeDefs()[0].id);beginTrial();resolveTrial('resources');check(s.crisisResult.level===0&&s.crisisResult.lifeLine.includes('未能存活')&&!s.crisisResult.lifeLine.includes('存活了下来'),'failure truth');
print('life moments, first purchase, nine combinations, history, opening and failure OK');return;\n'''
source=source.replace("  $('closeOffline').addEventListener('click'",test+"  $('closeOffline').addEventListener('click'",1)
jsc=shutil.which('jsc') or '/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
with tempfile.TemporaryDirectory() as folder:
 script=Path(folder)/'life.js';script.write_text(prefix+source);subprocess.run([jsc,str(script)],check=True)
