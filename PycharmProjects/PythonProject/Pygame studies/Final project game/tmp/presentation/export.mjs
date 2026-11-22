import fs from 'node:fs/promises';
import { Presentation, PresentationFile } from 'file:///C:/Users/DELL/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
import { finalizePresentation } from 'file:///C:/Users/DELL/.codex/plugins/cache/openai-primary-runtime/presentations/26.1104.12130/skills/presentations/container_tools/artifact_tool_utils.mjs';

const root = 'C:/Users/DELL/PycharmProjects/PythonProject/Pygame studies/Final project game';
const build = root + '/tmp/presentation';
const out = root + '/output/presentation';
const skill = 'C:/Users/DELL/.codex/plugins/cache/openai-primary-runtime/presentations/26.1104.12130/skills/presentations';
process.env.RUNTIME_NODE_MODULES = 'C:/Users/DELL/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const proto = JSON.parse(await fs.readFile(build + '/deck-export.json', 'utf8'));
proto.images = proto.images.map(i => ({...i, data: Uint8Array.from(i.data), uri: undefined}));
const presentation = Presentation.load(proto);
const candidatePath = build + '/candidate.pptx';
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
await finalizePresentation({
  workspaceDir: root,
  candidatePath,
  finalPath: out + '/Tank_Shooters_Presentation.pptx',
  explicitTotalSlideCount: 6,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [],
  pythonExecutable: 'C:/Users/DELL/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
  integrityValidatorPath: skill + '/container_tools/inspect_presentation_package_integrity.py',
  layoutValidatorPath: skill + '/container_tools/inspect_presentation_layout_geometry.py',
  layoutArgs: ['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],
  fontPolicy: {basis:'design',families:['Arial']},
  verifyArtifactToolImport: true,
  receiptPath: build + '/validation.json',
});
console.log('Exported six-slide editable PPTX.');
