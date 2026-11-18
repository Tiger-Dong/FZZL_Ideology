# coding: utf-8
from pathlib import Path
s=(Path(__file__).resolve().parents[1] / 'index.html').read_text().split('<script>')[1].split('</script>')[0]
prefix='var navigator={language:"zh"};var document={documentElement:{},getElementById:function(){return {}}};var localStorage={getItem:function(){return null},setItem:function(){}};var performance={now:function(){return 0}};\n'
test='''render=()=>{};toast=()=>{};save=()=>{};function check(v,m){if(!v)throw Error(m)}
s=fresh();s.mode='growth';s.thoughts=99;s.runThoughts=100;unlockMindEvolution('sprout');check(!s.mindEvolutions.sprout,'need spend');s.thoughts=100;unlockMindEvolution('sprout');check(s.mindEvolutions.sprout&&s.thoughts===0,'unlock');s.thoughts=1500;check(synthesizeNode()&&s.thoughts===1400&&s.mind===1,'node consumes');check(Math.abs(thoughtInterval()-3/1.0001)<1e-10,'node speed');for(let i=0;i<9;i++)synthesizeNode();check(s.mind===10&&!synthesizeNode(),'cap10');s.thoughts=100;unlockMindEvolution('knowledge');check(nodeCapacity()===20&&s.thoughts===0,'knowledge cap');
s=fresh();s.mode='world';s.worldview='magic';s.species='human';s.raceResources={mana:1000};s.runThoughts=1000;s.network=true;s.mindEvolutions.sprout=true;s.storage.mind=2;s.thoughts=1500;s.savedAt=1000;let r=settleOffline(31000);check(r.nodes===3&&s.mind===3,'offline nodes');check(s.thoughts===1210,'offline spends and gains');check(settleOffline(31000)===null,'offline no double');
for(const sp of ['human','animal','plant'])for(const w of ['magic','cultivation','technology']){s=fresh();s.mode='world';s.species=sp;s.worldview=w;s.raceResources={[worlds[w].currency]:1000};const defs=raceEvolutionDefs[sp];unlockRaceEvolution(defs[1].id);check(!s.raceEvolutions[defs[1].id],'prerequisite');for(const def of defs)unlockRaceEvolution(def.id);check(defs.every(x=>raceEvolutionUnlocked(x.id)),'all abilities '+sp+w);unlockWorldEvolution();check(raceEvolutionUnlocked(worldEvolutionDefs[w].id),'world ability '+w)}
s=fresh();s.mode='world';s.species='animal';s.worldview='magic';s.raceResources={mana:100};s.raceEvolutions={strength:true,survival:true,constitution:true};s.network=true;beginTrial();resolveTrial('resources');check(s.crisisResult.level===2,'animal powers change event');
s=fresh();s.mode='world';s.species='human';s.worldview='magic';s.raceResources={mana:100};s.raceEvolutions={creativity:true};check(crisisPrepCost('protect')===6,'discount');prepareCrisis('protect');check(s.raceResources.mana===94,'discount charged');
print('node unlock, cost, capacity, speed, offline synthesis, 9 species/world combinations and abilities OK');return;\n'''
s=s.replace("  $('closeOffline').addEventListener('click'",test+"  $('closeOffline').addEventListener('click'",1);import shutil, subprocess, tempfile
jsc=shutil.which('jsc') or '/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
with tempfile.TemporaryDirectory() as folder:
    script=Path(folder)/'growth.js'
    script.write_text(prefix+s)
    subprocess.run([jsc,str(script)],check=True)

