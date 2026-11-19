from pathlib import Path
import subprocess, tempfile, shutil
html=(Path(__file__).resolve().parents[1]/'index.html').read_text()
source=html.split('<script>')[1].split('</script>')[0]
prefix='''var navigator={language:'zh'};function element(){return {hidden:false,textContent:'',innerHTML:'',children:[],classList:{toggle:function(){}},append:function(){this.children.push.apply(this.children,arguments)},querySelector:function(){return element()},querySelectorAll:function(){return []}}}var nodes={};var document={documentElement:{},getElementById:function(id){return nodes[id]||(nodes[id]=element())},createElement:element};var localStorage={getItem:function(){return null},setItem:function(){}};var performance={now:function(){return 0}};
'''
test='''render=()=>{};toast=()=>{};save=()=>{};polishUpgradeCards=()=>{};
function check(v,m){if(!v)throw Error(m)}function content(e){return e.textContent+e.innerHTML+e.children.map(content).join('')}
function draw(tab){s.upgradeTab=tab;$('upgradeList').children=[];renderUpgrades();return content(nodes.upgradeList)}
s=fresh();s.mode='growth';s.runThoughts=1000;s.thoughts=1000;check(draw('explore').includes('选择生命载体'),'carrier selection reachable');check(!nodes.upgradeTabs.innerHTML.includes('回响恒铸')&&!nodes.upgradeTabs.innerHTML.includes('载体'),'locked modules hidden');
for(const sp of ['human','animal','plant'])for(const w of ['magic','cultivation','technology']){s=fresh();s.mode='world';s.species=sp;s.worldview=w;s.runThoughts=2000;s.network=true;s.raceResources={[worlds[w].currency]:300};check(draw('thought').includes('灵感'),'mind unlock reachable');check(draw('species').includes('载体'),'carrier upgrades');check(draw('explore').includes('生命的萌芽'),'life unlock reachable');check(draw('trial').includes('信息收集'),'trial reachable');s.upgradeTab='special';renderUpgrades();check(s.upgradeTab==='explore','old tab migration')}
s.mode='summary';s.echo=10;const text=draw('legacy');check(text.includes('思维仓库'),'permanent upgrade reachable');check(!text.includes('生命的萌芽')&&!text.includes('解锁 · 200 念头'),'no run upgrades in summary');
check(redesignEncyclopediaEntries().some(x=>x.id==='plant-awakening'),'planned routes documented');print('five module routing, nine combinations, old tabs and summary filtering OK');return;
'''
source=source.replace("// UI_EVENTS_BEGIN",test+"// UI_EVENTS_BEGIN",1)
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'modules.js';p.write_text(prefix+source)
 subprocess.run([shutil.which('jsc') or '/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc',str(p)],check=True)
