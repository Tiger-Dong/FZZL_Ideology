from pathlib import Path
import subprocess, tempfile, shutil
html=(Path(__file__).resolve().parents[1]/'index.html').read_text();source=html.split('<script>')[1].split('</script>')[0]
prefix='var navigator={language:"zh"};var document={documentElement:{},getElementById:function(){return {}}};var localStorage={getItem:function(){return null},setItem:function(){}};var performance={now:function(){return 0}};\n'
test='''render=()=>{};toast=()=>{};save=()=>{};function check(v,m){if(!v)throw Error(m)}
s=fresh();s.mode='growth';let entries=encyclopediaIndex();check(entries.some(e=>e.name==='念头')&&!entries.some(e=>e.name==='知识节点')&&!entries.some(e=>e.name==='魔力'),'early encyclopedia hides future resources');check(entries.some(e=>e.id==='next-resource-hint'&&e.summary.includes('思维萌芽')),'next resource hint');s.mindEvolutions.sprout=true;entries=encyclopediaIndex();check(entries.some(e=>e.name==='知识节点')&&!entries.some(e=>e.name==='思绪链接'),'node discovery');s.mindEvolutions.knowledge=true;entries=encyclopediaIndex();check(entries.some(e=>e.name==='思绪链接'),'link discovery');
s=fresh();s.mode='growth';check(!outputAvailable('frequency'),'frequency locked');s.runThoughts=49;check(!outputAvailable('network'),'inspiration locked before 50');s.runThoughts=50;check(outputAvailable('network')&&!outputAvailable('frequency')&&!outputAvailable('growth'),'inspiration unlocks at 50');s.runThoughts=100;check(outputAvailable('frequency')&&outputAvailable('growth'),'output unlocks at 100');s.thoughts=1000;check(upgradeCost('frequency')===150,'cost');buyUpgrade('frequency');check(s.thoughts===850&&frequencyFactor()===.9,'frequency');s.runThoughts=200;buyUpgrade('growth');check(growthYield()===6,'growth +5');s.runThoughts=100;buyUpgrade('network');check(clickThoughtYield()===6,'inspiration is independent of growth');let automaticBefore=thoughtYield(), clickBefore=clickThoughtYield();s.amountLv++;check(clickThoughtYield()===clickBefore&&thoughtYield()===automaticBefore+5,'growth affects automatic yield only');s.networkLv++;check(clickThoughtYield()===clickBefore+5&&thoughtYield()===automaticBefore+5,'inspiration affects click yield only');check(upgradeCap('growth')===30,'growth cap');
s=fresh();s.mode='growth';s.runThoughts=500;s.thoughts=1000;unlockMindEvolution('sprout');check(s.mindEvolutions.sprout&&s.thoughts===0,'sprout cost');s.thoughts=500;check(synthesizeNode()&&s.thoughts===0&&s.totalNodes===1,'node consume');s.mind=10;check(!synthesizeNode(),'capacity no consume');s.storage.mind=10;s.thoughts=2000;s.totalNodes=10;unlockMindEvolution('knowledge');check(s.mind===5&&s.thoughts===0&&nodeCapacity()===20,'knowledge');convertMind('link');check(s.mind===2&&s.networkLinks===1&&s.totalLinks===1,'link');s.networkLinks=5;s.mind=10;s.thoughts=5000;convertMind('link');check(s.networkLinks===5&&s.mind===10,'full link no consume');buyCapacity('link');check(linkCapacity()===10,'link expansion');
for(const sp of ['human','animal','plant'])for(const w of ['magic','cultivation','technology']){s=fresh();s.mode='world';s.species=sp;s.worldview=w;s.raceResources={[worlds[w].currency]:100000};const d=raceStatDefs()[0];check(raceUpgradeCost(d.id)===200,'first stat cost');buyUpgrade(d.id);check(s.raceBase[d.id]===1&&s.raceStats[d.id]===1,'base +1');for(let i=0;i<9;i++)buyUpgrade(d.id);check(pendingTraits().some(x=>x.threshold===10),'trait unlocked');const held=s.raceBase[d.id],wallet=s.raceResources[worlds[w].currency];buyUpgrade(d.id);check(s.raceBase[d.id]===held,'pending trait blocks upgrade');chooseTrait(d.id,10);check(s.raceResources[worlds[w].currency]===wallet-1000,'trait cost');check(s.raceBase[d.id]===10&&s.raceTraitBonus[d.id]===3&&s.raceStats[d.id]===13,'trait isolated');chooseTrait(d.id,10);check(s.raceStats[d.id]===13,'trait once')}
s=fresh();s.mode='world';s.worldview='magic';s.species='human';const currency=worlds.magic.currency,high=worlds.magic.resources.find(x=>x[3]>0)[0];s.raceResources={[currency]:1000};check(raceCapacity(currency)===5000&&raceCapacity(high)===20,'initial race capacities');check(storageCost('race')===1000&&!storageRequirement('race'),'first expansion available');buyStorage('race');check(raceCapacity(currency)===7000&&raceCapacity(high)===2020&&storageCost('race')===1100&&s.raceResources[currency]===0,'race storage upgrade');const stat=raceStatDefs()[0];s.raceUpgrades[stat.id]=9;check(raceUpgradeCost(stat.id)<=raceCapacity(currency),'tenth stat upgrade affordable after expansion');
s=fresh();s.mode='world';s.worldview='magic';s.species='human';s.raceResources={mana:1000};s.runThoughts=1000;s.thoughts=1000;startDetection();check(planLimit()===1,'unknown cap');chooseTrialDirection('protect');draftTrialPlan();check(s.trialPlan.plans[0].direction==='protect','own direction');implementTrialPlan(0,1);check(s.trialPlan.plans[0].completion===1/3,'partial');const before=s.raceResources.mana;implementTrialPlan(0,1);check(s.raceResources.mana===before,'no repeat step');implementTrialPlan(0,2);implementTrialPlan(0,3);check(s.trialPlan.plans[0].completion===1,'complete');check(coverage()===1,'single direction');s.stageUnlocks.infoArchive=true;s.crisisIntel['magic:basic']=3;check(intelTier()===4,'91 archive rule');
s=fresh();s.mode='summary';s.echo=9;check(stageChoices().find(x=>x.id==='worldChoice').locked,'world choice requires developed population');s.tribeDeveloped=true;buyStageChoice('worldChoice');check(s.stageUnlocks.worldChoice&&s.echo===6,'world choice purchase');buyStageChoice('branch');check(s.stageUnlocks.branch&&s.echo===3,'specialization purchase');s.mode='species';s.runThoughts=1000;chooseSpecies('human','technology');check(s.worldview==='technology'&&raceEvolutionUnlocked('technology-sensor'),'selected world and automatic ability');check(raceEvolutionCost(0)===150,'carrier ability cost');
s=fresh();s.mode='summary';s.echo=10;buyStageChoice('mindStorage');check(s.echo===9&&thoughtCapacity()===15000,'legacy');s.savedAt=1000;s.thoughts=10;check(settleOffline(900000)===null&&s.thoughts===10,'summary frozen');
s=fresh();s.mode='world';s.worldview='magic';s.species='human';s.savedAt=1000;s.raceResources={mana:0};s.spiritLanguageLv=2;s.legacyBoosts.resourceFlow=1;const gain=settleOffline(11000);check(s.raceResources.mana===161,'offline +5 flow and spirit with multiplier');check(gain.thoughts>=50,'offline thought flow +5');
s=fresh();s.mode='growth';s.savedAt=1000;s.runThoughts=999;s.thoughts=999;const cross=settleOffline(61000);check(cross.used===60&&s.mode==='species'&&s.runThoughts>1000,'offline continues after carrier threshold');const accumulated=s.runThoughts;s.savedAt=61000;const waiting=settleOffline(121000);check(waiting.used===60&&s.runThoughts>accumulated,'offline continues while carrier choice pending');
s=fresh();s.mode='growth';s.savedAt=1000;s.runThoughts=500;s.mindEvolutions.sprout=true;s.thoughts=500;const r=settleOffline(31000);check(r.nodes===1&&s.mind===1,'30 second offline synthesis');
for(const sp of ['human','animal','plant'])for(const w of ['magic','cultivation','technology']){
  s=fresh();s.mode='species';s.runThoughts=1700;s.thoughts=1700;s.stageUnlocks.worldChoice=true;
  chooseSpecies(sp,w);
  const currency=currentRaceCurrency(), route=firstCarrierRoutes[sp];
  s.raceResources[currency]=route.cost.carrier-1;
  check(!learnFirstCarrierRoute()&&!s.trialPlan.carrierPractice&&s.raceResources[currency]===route.cost.carrier-1,'carrier training checks inventory');
  s.raceResources[currency]=302;
  check(!firstTrialPreparation().trained&&!s.trialPlan.started,'new practice visible before countdown');
  check(learnFirstCarrierRoute()&&s.raceResources[currency]===302-route.cost.carrier,'carrier practice real cost before countdown');
  check(!learnFirstCarrierRoute(),'cannot train twice');
  unlockMindEvolution('sprout');check(synthesizeNode()&&!s.network,'first node before any network');
  startDetection();chooseTrialDirection(trialWorldFocus[w]);draftTrialPlan();
  check(!implementTrialPlan(0,1,true),'tool never applies to the wrong step');
  implementTrialPlan(0,1);
  check(crisisAssessment(trialOptions()[0]).level===0,'one implemented step cannot satisfy any of the three routes');
  implementTrialPlan(0,2);
  if(sp==='human'){
    check(crisisAssessment(trialOptions()[0]).level===0&&!implementTrialPlan(0,3),'human still needs to deploy the tool');
    check(implementTrialPlan(0,3,true)&&!implementTrialPlan(0,3,true)&&s.trialPlan.plans[0].stepCosts[3]===0,'tool completes the third step for free exactly once');
  }else if(sp==='animal'){
    check(crisisAssessment(trialOptions()[0]).level===0&&!implementTrialPlan(0,3,true),'animal still needs third step and cannot use the tool');
    implementTrialPlan(0,3);
  }else{
    check(trialPlanCompletion(s.trialPlan.plans[0])===2/3&&!s.trialPlan.plans[0].firstTool,'plant relies on roots without faking third-step completion');
  }
  check(s.thoughts===0&&s.raceResources[currency]===0,'all three routes have the same baseline budget');
  check(s.trialPlan.plans[0].quality===1&&crisisAssessment(trialOptions()[0]).level===1,'all nine basic carrier routes survive with one node');
  const practice=s.trialPlan.carrierPractice;
  delete s.trialPlan.carrierPractice;
  check(crisisAssessment(trialOptions()[0]).level===0,'the new route requires its special preparation');
  s.trialPlan.carrierPractice=practice;
  s.mind=s.totalNodes=0;
  check(crisisAssessment(trialOptions()[0]).level===0,'first survival still requires a formed knowledge node');
  s.mind=s.totalNodes=1;
  s.trialPlan.plans[0].direction=Object.keys(trialDirections).find(id=>id!==trialWorldFocus[w]);
  check(crisisAssessment(trialOptions()[0]).level===0,'fully implemented but mismatched plan does not guarantee survival');
  s.trialPlan.plans[0].direction=trialWorldFocus[w];
  s.cycle=2;check(crisisAssessment(trialOptions()[0]).level===0,'introductory survival route is first-round only');s.cycle=1;
  chooseTrialDirection(Object.keys(trialDirections).find(id=>id!==trialWorldFocus[w]));
  check(resolveTimedTrial()&&s.mode==='summary'&&s.crisisResult.level===1,'resolve through timed trial entry point');
  const history=s.cycleHistory.at(-1), echo=s.echo;
  check(history.recap[1][1].includes('知识节点')&&history.recap[1][1].includes(route.outcome),'recap explains the actual species-specific path');
  check(history.crisis.spending[0].includes(route.name),'records the special preparation and the charge');
  check(history.crisis.newClues.length&&echo===history.reward,'discovery and echo are awarded and archived');
  check(!resolveTimedTrial()&&s.echo===echo&&s.cycleHistory.length===1,'settlement cannot reward the same event twice');
}
s=fresh();s.mode='world';s.species='human';s.worldview='magic';s.totalNodes=1;s.raceUpgrades['race-magic-human-0']=1;
s.trialPlan={started:true,deadline:Date.now()+60000,plans:[{direction:'protect',quality:1,applied:true,completion:1}]};
check(!firstTrialPreparation().route&&crisisAssessment(trialOptions()[0]).level===1,'an already-started legacy trial keeps its old survival route');
s=fresh();s.mode='world';s.species='plant';s.worldview='magic';s.runThoughts=1000;s.thoughts=1000;s.raceResources.mana=250;
startDetection();chooseTrialDirection('study');draftTrialPlan();
check(resolveTimedTrial()&&s.crisisResult.level===0&&s.echo>0&&s.cycleHistory[0].recap[0][1].includes('未能存活'),'unprepared failure still reaches settlement');
function trialFixture(species, world, developed=false) {
  s=fresh();s.mode='world';s.cycle=2;s.species=species;s.worldview=world;s.thoughts=3000;
  s.raceResources[currentRaceCurrency()]=3000;
  s.raceEvolutions[worldEvolutionDefs[world].id]=true;
  if(developed){s.network=true;s.raceUpgrades[raceStatDefs()[0].id]=1}
  return currentRaceCurrency();
}
function trialQuote(id){return crisisActions().find(option=>option.id===id).cost}
let cur=trialFixture('human','magic',true);
check(!prepareCrisis('reserve'),'paid preparation waits for observation');
check(startDetection()&&s.thoughts===3000&&s.raceResources[cur]===3000,'initial observation is free');
check(crisisAssessment(trialOptions()[0]).level===0,'without preparation the developed carrier fails');
check(trialQuote('reserve').carrier===500&&prepareCrisis('reserve')&&s.raceResources[cur]===2500,'reserve charges the displayed price');
check(!prepareCrisis('reserve')&&s.raceResources[cur]===2500,'reserve cannot charge twice');
check(crisisAssessment(trialOptions()[0]).level===1,'reserve changes the survival outcome');
cur=trialFixture('human','magic',true);startDetection();
s.thoughts=499;check(!prepareCrisis('protect')&&s.raceResources[cur]===3000,'no carrier charge if thoughts are short');
s.thoughts=500;s.raceResources[cur]=499;
check(!prepareCrisis('protect')&&s.thoughts===500&&!s.crisisPrep.length,'no thought charge if carrier stock is short');
s.thoughts=3000;s.raceResources[cur]=3000;
check(!prepareCrisis('unknown'),'reject unknown preparation');
check(prepareCrisis('protect')&&s.thoughts===2500&&s.raceResources[cur]===2500,'mixed payment charges each resource exactly once');
check(crisisAssessment(trialOptions()[0]).level===1,'one paid direction does not cover the disaster');
check(prepareCrisis('study')&&s.thoughts===2000&&s.crisisPrepPaid.study.intelGain===1,'study payment raises intel');
check(crisisAssessment(trialOptions()[0]).level===3,'study records and separate protection contribute to the outcome');
check(resolveTimedTrial()&&s.cycleHistory[0].crisis.spending.some(line=>line.includes('500 念头 + 500 魔力')&&line.includes('参与抵御')),'settlement records paid resources and actual protection');
cur=trialFixture('plant','technology');startDetection();
check(!deepenObservation()&&intelTier()===0,'deeper observation is optional and needs knowledge');
s.society.knowledge=2;check(deepenObservation()&&s.society.knowledge===1&&intelTier()===1&&planLimit()===2,'knowledge payment changes tactical limit');
check(!deepenObservation()&&s.society.knowledge===1,'deeper observation cannot charge twice');
chooseTrialDirection('study');check(draftTrialPlan()&&s.thoughts===2800,'first draft payment');
check(trialQuote('study').thought===350&&prepareCrisis('study')&&s.thoughts===2450,'environment monitoring halves paid organization');
s.raceEvolutions.carbon=true;check(trialQuote('reserve').carrier===400&&prepareCrisis('reserve')&&s.raceResources[cur]===2600,'carbon halves reserve realization cost');
check(implementTrialPlan(0,1)&&s.raceResources[cur]===2588&&s.trialPlan.plans[0].stepCosts[1]===12,'implementation consumes the listed resource');
check(Math.abs(appliedPlanStrength(s.trialPlan.plans[0])-1/3)<1e-9,'matched step contributes one third of grade');
check(draftTrialPlan()&&s.thoughts===2150&&s.trialPlan.plans[1].cost===300,'second draft price increases by 1.5');
s.stageUnlocks.infoArchive=true;s.crisisIntel[crisisKey()]=3;
check(planStepCost(2)===24&&implementTrialPlan(0,2)&&s.raceResources[cur]===2564,'archive discount applies to the charged step');
check(s.trialPlan.plans[0].stepCosts[1]===12&&s.trialPlan.plans[0].stepCosts[2]===24,'historic charges do not reprice');
s.trialPlan.deadline=Date.now()-1;
check(!draftTrialPlan()&&!prepareCrisis('protect')&&!implementTrialPlan(0,3)&&s.raceResources[cur]===2564,'late payments rejected');
check(resolveTimedTrial()&&s.cycleHistory[0].crisis.plans[0].stepCosts[2]===24,'charged amounts reach the archived result');
cur=trialFixture('human','magic');s.raceEvolutions.creativity=true;startDetection();chooseTrialDirection('protect');draftTrialPlan();
check(prepareCrisis('protect')&&s.thoughts===2200&&s.raceResources[cur]===2700,'creativity halves only the carrier part of a mixed quote');
print('v016 progression, offline play, nine introductory paths and trial payments and outcomes OK');return;
'''
source=source.replace("// UI_EVENTS_BEGIN",test+"// UI_EVENTS_BEGIN",1)
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'v016.js';p.write_text(prefix+source);subprocess.run([shutil.which('jsc') or '/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc',str(p)],check=True)
