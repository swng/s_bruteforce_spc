const { decoder, encoder, Mino, Field} = require('tetris-fumen');
const {make_sys_call} = require('./make_sys_call.js');


async function generate(base_field, hold_piece) {
    let results = new Set();

    for (let col = 0; col < 10; col++) {
        for (let row = 0; row < 6; row++) {
            for (let rotation_state of ['spawn', 'right']) { // don't need reverse and left for S placements, they're effectively congruent after placement
                let mino = new Mino(hold_piece, rotation_state, col, row);
                if (mino.isValid()) {
                    let field = base_field.copy();
                    if (field.canLock(mino)) {
                        let positions = mino.positions();
                        good = true;
                        for (position of positions) {
                            if (position.y >= 6) good = false;
                        }
                        if (good) {
                            // field.put(mino);
                            for (let position of mino.positions()) {
                                field.set(position.x, position.y, hold_piece);
                            }
                            // field = grey_out(field);
                            results.add(encoder.encode([{
                                field: field
                            }]))
                        }
                    }
                }

            }
        }
    }

    return results;

}

async function main() {
    let empty_field = Field.create('');
    let results = await generate(empty_field, 'S');
    
    let index = 0;
    for (let result of results) { // 17 initial S placements
        // java -jar sfinder.jar spin -p '*p7' -fb 0 -ft 4 -m 6 -c 1 -t 'v115@Rhg0Iei0QeAgH'
        let command = `java -jar sfinder.jar spin -p '*p7' -fb 0 -ft 4 -m 6 -c 1 -t ${result} -o spin_files/s_spc_${String(index).padStart(2, '0')}.html`
        // console.log(command);
        await make_sys_call(command);
        index++;
    }
}

main();