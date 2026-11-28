"""Regression checks for upgrade metadata and progressive disclosure using JavaScriptCore."""
from pathlib import Path
import subprocess
import tempfile
import shutil

source = (Path(__file__).resolve().parents[1] / 'index.html').read_text().split('<script>')[1].split('</script>')[0]
prefix = '''
var navigator={language:'zh'};
function element(){var markup='';var e={hidden:false,textContent:'',style:{},dataset:{},setAttribute:function(){},children:[],classList:{toggle:function(){}},append:function(){this.children.push.apply(this.children,arguments)},querySelector:function(){return element()},querySelectorAll:function(){return []}};Object.defineProperty(e,'innerHTML',{get:function(){return markup},set:function(v){markup=v;this.children=[]}});return e}
var nodes={};var document={documentElement:{},getElementById:function(id){return nodes[id]||(nodes[id]=element())},createElement:element};
var localStorage={getItem:function(){return null},setItem:function(){}};var performance={now:function(){return 0}};
'''
test = '''
render=()=>{};toast=()=>{};save=()=>{};polishUpgradeCards=()=>{};renderStoryLog=()=>{};updateWorldDataView=()=>{};
function check(v,m){if(!v)throw Error(m)}
function content(e){return e.textContent+e.innerHTML+e.children.map(content).join('')}
function draw(tab){s.upgradeTab=tab;renderUpgrades();return content($('upgradeList'))}
function resources(){renderResources();return $('resourceRows').innerHTML}
s=fresh();s.mode='growth';s.runThoughts=49;renderGoalHud();check(nodes.goalTitle.textContent==='让念头成形'&&nodes.goalDetail.textContent.includes('50'),'goal before 50');s.dismissedGuide=nodes.guideToggle.dataset.step;renderGoalHud();check(nodes.goalDetail.hidden,'individual guidance collapses');s.runThoughts=50;renderGoalHud();check(!nodes.goalDetail.hidden&&nodes.goalDetail.textContent.includes('100'),'next step shown at 50');s.runThoughts=100;renderGoalHud();check(nodes.goalDetail.textContent.includes('500')&&nodes.goalDetail.textContent.includes('1000'),'sprout goal');s.runThoughts=1000;renderGoalHud();check(nodes.goalTitle.textContent==='选择生命载体'&&nodes.guideOpenModule.dataset.tab==='explore','carrier goal leads to the correct module');s.guideHints=false;renderGoalHud();check(nodes.guideOpenModule.hidden&&nodes.goalDetail.hidden&&!nodes.goalHud.hidden,'progress stays visible with hints off');s.guideHints=true;s.species='human';s.worldview='magic';s.mode='world';renderGoalHud();check(nodes.goalDetail.textContent.includes('信息收集'),'trial available goal');s.trialPlan.started=true;s.trialPlan.deadline=Date.now()+60000;renderGoalHud();check(nodes.goalDetail.textContent.includes('方案方向'),'choose direction goal');s.trialPlan.direction='protect';renderGoalHud();check(nodes.goalDetail.textContent.includes('200'),'draft cost goal');draftTrialPlan();s.thoughts=200;draftTrialPlan();let trial=draw('trial');check(trial.includes('已落实 0 / 3 项')&&trial.includes('还差 60 魔力')&&trial.includes('防护 · 浮动的边缘'),'actual plan steps, direction and shortfall');
s=fresh();s.mode='world';s.species='human';s.worldview='magic';s.thoughts=499;s.raceResources.mana=499;
check(draw('trial').includes('开始信息收集 · 免费'),'free detection shown');
startDetection();trial=draw('trial');
check(trial.includes('归纳整理')&&trial.includes('防护预案')&&trial.includes('资源储备')&&trial.includes('准备 · 500 念头 + 500 魔力')&&trial.includes('还差 1 念头 + 1 魔力'),'joint shortage and exact prices shown');
s.society.knowledge=1;check(draw('trial').includes('观测 · 1 知识'),'paid observation uses knowledge');
s.thoughts=2000;s.raceResources.mana=2000;chooseTrialDirection('protect');draftTrialPlan();prepareCrisis('protect');implementTrialPlan(0,1);
trial=draw('trial');check(trial.includes('已投入 600 念头 + 600 魔力')&&trial.includes('已落实 · 12 魔力')&&trial.includes('仅用于保全结算'),'display actual charged amounts and explain retention');
for(const sp of ['human','animal','plant']){
 s=fresh();s.mode='world';s.species=sp;s.worldview='magic';s.thoughts=1000;s.raceResources.mana=200;
 const route=firstCarrierRoutes[sp];trial=draw('trial');
 check(trial.includes(route.name)&&trial.includes('1700 念头 + 302 魔力')&&trial.includes('还差 700 念头 + 102 魔力')&&trial.includes('查看发展探索'),'pre-countdown checklist names route, entry and exact shortfalls');
 check(draw('explore').includes(route.name)&&draw('explore').includes('准备 · '+route.cost.carrier+' 魔力'),'carrier preparation has a real purchase card');
 s.raceResources.mana=302;learnFirstCarrierRoute();s.totalNodes=1;renderGoalHud();
 check(draw('trial').includes('已具备 · '+route.name)&&draw('trial').includes('200 念头 + '+(302-route.cost.carrier)+' 魔力'),'pre-countdown shows only remaining costs');
 startDetection();chooseTrialDirection('protect');draftTrialPlan();trial=draw('trial');
 check(trial.includes('使用应变工具 · 免费')===(sp==='human')&&trial.includes('循迹辨险：你已辨出')===(sp==='animal'),'only the right carrier sees its action or direction hint');
 implementTrialPlan(0,1);implementTrialPlan(0,2);renderGoalHud();
 check(nodes.goalDetail.textContent.includes('基础幸存准备已齐')===(sp==='plant'),'rooted carrier gains readiness before full completion');
}
s=fresh();s.mode='growth';let text=draw('thought');check(!text.includes('思绪流动')&&!text.includes('思念拓展')&&!text.includes('知识汇聚'),'early upgrades hidden');
text=resources();check(text.includes('data-res="thought"')&&!text.includes('data-res="mind"')&&!text.includes('data-res="networkLinks"')&&!text.includes('data-res="networkCount"')&&!text.includes('data-res="ideology"'),'only available thought resources');
s.resourceSettingsOpen=true;check(!resources().includes('data-resource-visible="mind"'),'settings cannot expose locked resources');
s.runThoughts=50;text=draw('thought');check(text.includes('灵感')&&text.includes('Lv.0 / 15')&&text.includes('点击 1 → 6')&&text.includes('升级 · 200 念头'),'click upgrade metadata without affordability');check(!text.includes('思绪流动')&&!text.includes('思想萌发'),'later output hidden');
s.runThoughts=100;text=draw('thought');check(text.includes('思绪流动')&&text.includes('思想萌发'),'both unlock at 100');
s.runThoughts=500;s.thoughts=1000;text=draw('thought');check(text.includes('基础提升 · 资源产出')&&text.includes('进阶拓展 · 转化与能力'),'mind categories');check(text.includes('间隔 3000 → 2700 毫秒')&&text.includes('升级 · 150 念头')&&text.includes('需要：1000 念头、0 节点、0 链接'),'output and evolution costs');check(!text.includes('知识汇聚')&&!text.includes('思念拓展'),'evolution prerequisites respected');
buyUpgrade('frequency');text=draw('thought');check(text.includes('Lv.1 / 10')&&text.includes('升级 · 200 念头')&&text.includes('间隔 2700 → 2633 毫秒'),'metadata changes after actual purchase');
s.thoughts=1000;unlockMindEvolution('sprout');text=draw('thought');check(text.includes('基础提升 · 容量存储')&&text.includes('思念拓展')&&text.includes('10000 → 15000')&&!text.includes('知识汇聚'),'storage revealed by sprout');
text=resources();check(text.includes('data-res="mind"')&&!text.includes('data-res="networkLinks"'),'node resource appears after sprout');
s.totalNodes=10;s.mind=10;text=draw('thought');check(text.includes('知识汇聚')&&text.includes('需要：2000 念头、5 节点、0 链接'),'unaffordable evolution stays visible');check(text.includes('思绪凝聚'),'node capacity revealed');s.mind=0;check(draw('thought').includes('思绪凝聚'),'revealed capacity survives spending');
s.thoughts=2000;s.mind=5;unlockMindEvolution('knowledge');text=resources();check(text.includes('data-res="networkLinks"')&&!text.includes('data-res="networkCount"'),'link unlock distinct from network');
for(const sp of ['human','animal','plant'])for(const w of ['magic','cultivation','technology']){
 s=fresh();s.mode='world';s.species=sp;s.worldview=w;s.raceResources={[worlds[w].currency]:0};text=draw('species');check(text.includes('基础提升')&&text.includes('进阶拓展'),'carrier categories');check(text.includes('Lv.0 / 10')&&text.includes('总值 0 → 1')&&text.includes('升级 · '),'carrier metadata');const defs=raceEvolutionDefs[sp];check(text.includes(defs[0].name)&&!text.includes('<strong>'+defs[1].name+'</strong>'),'only available carrier abilities');
 text=resources();check(text.includes('data-res="'+worlds[w].currency+'"'),'base carrier currency visible');for(const [id] of worlds[w].resources.slice(1))check(!text.includes('data-res="'+id+'"'),'locked carrier currency hidden: '+id);
 s.raceEvolutions[defs[0].id]=true;check(draw('species').includes(defs[1].name),'next ability revealed');
}
s=fresh();s.mode='summary';s.echo=0;text=draw('legacy');check(text.includes('永久念头容量加成 0 → 5000')&&text.includes('升级 · 1 回响')&&text.includes('Lv.0 / 持续扩展'),'legacy metadata');check(!text.includes('<strong>思维迅捷</strong>'),'locked legacy hidden');
print('upgrade costs, levels, comparisons, categories, sequential unlocks, resources and nine carrier combinations OK');return;
'''
source = source.replace("// UI_EVENTS_BEGIN", test + "// UI_EVENTS_BEGIN", 1)
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / 'upgrade_visibility.js'
    path.write_text(prefix + source)
    subprocess.run([shutil.which('jsc') or '/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc', str(path)], check=True)
