"use strict";

import fs from 'fs';
import * as QALD from 'qald';
import Tp from 'thingpedia';
import ThingTalk from 'thingtalk';
import * as readline from 'readline';

const NLU_SERVER = 'http://127.0.0.1:8400/en-US/query';

async function main() {
    const tpClient = new Tp.FileClient({ thingpedia: './manifest.tt', locale: 'en' });
    const schemas = new ThingTalk.SchemaRetriever(tpClient, null, true);
    const classDef = await schemas.getFullMeta('wd');
    const domains = JSON.parse(fs.readFileSync('./domain.json', { encoding: 'utf8' })).data;

    const converter = new QALD.ThingTalkToSPARQLConverter(classDef, domains, {
        locale: 'en',
        timezone: 'utc',
        cache: 'wikidata_cache.sqlite',
        save_cache: true,
        bootleg: 'bootleg.sqlite',
        human_readable_instance_of: false
    });

    const wikidata = new QALD.WikidataUtils('wikidata_cache.sqlite', 'bootleg.sqlite', true);

    const fileStream = fs.createReadStream("../data/input/simple_questions.txt");

    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    var returnObj = {
        data: []
    }

    for await (const line of rl) {
        console.log(`Question: ${line}`);

        let thingtalk_output = null;
        let sparql_output = null;
        let final_answer = null;
        try {
            const nlu_result = await Tp.Helpers.Http.post(NLU_SERVER, JSON.stringify({ q: line }), {
                dataContentType: 'application/json'
            });
            const parsed = JSON.parse(nlu_result);
            if (parsed && parsed.candidates && parsed.candidates.length > 0)
                thingtalk_output = parsed.candidates[0].code.join(' ');
        } catch (e) {
            console.log(e.message);
        }

        if (!thingtalk_output) {
            console.log('Failed to parse the question. \n');
            thingtalk_output = "Failed to parse the question."
            rl.prompt();
        } else {
            console.log('ThingTalk:', thingtalk_output);
            try {
                sparql_output = await converter.convert(line, thingtalk_output);
                console.log('SPARQL:', sparql_output);
                try {
                    const answers = await wikidata.query(sparql_output);
                    console.log('Answers:');
                    if (answers.length === 0) {
                        final_answer = 'None'
                        console.log('None')
                    } else {
                        for (const answer of answers.slice(0, 5)) {
                            if (answer.startsWith('Q')) {
                                const label = await wikidata.getLabel(answer);
                                final_answer = label + " (" + answer + ")"
                                console.log(`${label} (${answer})`)
                            } else {
                                final_answer = answer
                                console.log(answer);
                            }

                        }
                        if (answers.length > 5)
                            console.log(`and ${answers.length - 5} more ...`)
                    }
                } catch (e) {
                    const failed_wikidata_message = 'Failed to retrieve answers from Wikidata.';
                    console.log(failed_wikidata_message);
                    console.log(e.message);
                    answer = failed_wikidata_message;
                }
            } catch (e) {
                const failed_sparql_message = 'Failed to convert thingtalk into SPARQL';
                console.log(failed_sparql_message);
                sparql = failed_sparql_message;
            }

        }
        console.log('\n');

        returnObj.data.push({
            question: line,
            thingtalk: thingtalk_output,
            sparql: sparql_output,
            answer: final_answer
        });

    }
    console.log(returnObj);

    var json = JSON.stringify(returnObj);
        fs.writeFile('../data/output/thingtalk_answer.json', json, 'utf8', function (err) {
            if (err) {return console.error(err);};
        });
}

main();