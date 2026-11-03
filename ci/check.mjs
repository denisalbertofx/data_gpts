import {readFileSync,appendFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
const {answer}=await import(pathToFileURL(process.cwd()+'/answer.mjs').href);
const expected=readFileSync('ci/expected.txt','utf8').trim(),got=String(await answer());
const summary=process.env.GITHUB_STEP_SUMMARY;
if(got!==expected){
 console.log(`::error file=answer.mjs,line=1,title=Contrato de cuatro campos::La decisión vigente es ${expected.split('|')[0]} (D2); la respuesta publicada es ${got}`);
 if(summary)appendFileSync(summary,`La decisión vigente es ${expected.split('|')[0]}; la respuesta publicada es ${got}.\n`);
 process.exit(1);
}
console.log('Contrato de cuatro campos cumplido: '+got);
