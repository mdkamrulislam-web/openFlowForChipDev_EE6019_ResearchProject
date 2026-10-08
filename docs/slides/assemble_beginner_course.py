from pathlib import Path
import json,re,hashlib
from copy import deepcopy
HERE=Path(__file__).resolve().parent
GUIDE=HERE.parent/'beginner-guide'
text=(GUIDE/'guide.md').read_text(encoding='utf-8')
REPO='https://github.com/mdkamrulislam-web/tt-sky130-counter'
SHA='61ef06bed008e76000f9ae46d65182e476d15dd6'
SOURCE=REPO+'/tree/'+SHA
TEMPLATE='https://github.com/TinyTapeout/ttsky-verilog-template'
front=[]
def add(id,title,layout,body,notes,heading='What you will learn and produce',**extra):
    front.append(dict(id=id,section='Start here',title=title,layout=layout,body=body,notes=notes,guide_heading=heading,sources=[SOURCE,'https://tinytapeout.com/hdl/templates/'],**extra))
add('F01','Your first Tiny Tapeout chip','cover',[],
    'This course follows one genuine eight-bit counter from its specification to a checked layout. Start with the circuit concepts even if you have programmed before: Verilog describes connected hardware, and the Python test is outside the fabricated design. Each lesson gives a small piece of understanding, a worked example and a check. The practical route uses your browser and a free GitHub account, while automated tools run on standard GitHub-hosted runners. It ends with an archived source revision and verified layout files. Submission, payment and wafer fabrication are explained afterwards as separate stages. No chip was ordered or manufactured for this example. Read the full Word manual for longer explanations and use the starter ZIP to preserve source paths and indentation. The chip picture here is an editable conceptual illustration, not a photograph or physical evidence.')
add('F02','What you will understand and produce','explain',[
    'Predict an eight-bit counter: reset, count, hold and wrap.',
    'Explain its Verilog, fixed chip interface and Python checks.',
    'Create a project and inspect the real automated results.',
    'Keep the source, datasheet, waveform and checked layout together.'
], 'A learning outcome is something you can explain or demonstrate. By the end you should predict the counter before running a simulator, identify which source statements implement those predictions and interpret the reported results without confusing simulation with silicon. The output package includes your saved source version, matching workflow links, XML result, actual waveform, generated datasheet, layout and check reports. A green icon alone is weaker than this connected evidence. The lesson uses a deliberately small design so arithmetic boundaries, reset priority and pin direction can be observed in detail. Bigger projects repeat the same reasoning but need additional specifications and tests. Work through the sections in order on the first pass. If a check fails, use the troubleshooting slides before moving ahead. Keep a plain-text evidence note beside the downloaded files.',example='One circuit.\n0 → 1 → 2 … 255 → 0\n\nOne checked revision.\nSeveral kinds of evidence.',check='You can name both the circuit behaviour and the files the exercise produces.')
add('F03','Your route through the course','flow',[],
    'The learning sequence is deliberate. Foundations make the binary output and clocked state understandable. The code lessons connect those ideas to the reusable counter, wrapper and cocotb test. The browser lab creates the repository and exposes the real results, including native captures from the actual RTL waveform. Physical design explains what the automated implementation did, which units appear in the reports and why timing, DRC, LVS and functional checks answer different questions. The fabrication lessons explain the free stopping point, dated costs and the later manufacturing chain. Optional local commands and exercises support further practice. This is a course-sized deck for study over several sessions, rather than a measured lab-duration claim. Use the contents and full manual to revisit a topic when a later result is unclear.',flow=[{'name':'01  Foundations','detail':'Bits, logic, stored state and clock edges'},{'name':'02  Read the code','detail':'Counter, wrapper and self-checking test'},{'name':'03  Browser lab','detail':'Template, files, workflows and real waves'},{'name':'04  Physical design','detail':'Cells, wires, timing and layout checks'},{'name':'05  Fabrication','detail':'Free endpoint, later order and silicon'},{'name':'06  Practise','detail':'Optional local setup and worked exercises'}])
add('F04','Get your learning workspace ready','explain',[
    'Use a laptop, browser, internet access and your own GitHub account.',
    'Keep counter-starter.zip and the Word manual beside this deck.',
    'Create tiny-tapeout-learning and an evidence folder for downloads.',
    'Use a public practice repository and standard Actions runners.'
], 'The main route needs no installed physical-design tools and no development container. A GitHub account lets you create your repository, commit files and download artifacts. Standard GitHub-hosted runner compute is free for public repositories; account storage and artifact policies still apply. The starter ZIP contains seven complete example files. It is added to a repository created from the official template, whose infrastructure supplies workflows and dependencies. Use the ZIP rather than copying printed code: visual wraps in documents do not represent real source newlines. Keep separate folders for source learning files and downloaded evidence so results from an older revision are less likely to be mistaken for the newest ones. Your account name replaces YOUR_USERNAME where a later command or URL uses that placeholder. Existing institutional accounts and branch rules should be respected.',heading='Keep these companion files together',check='You have the ZIP, manual, account and a place to save your evidence.')
add('F05','Understand the free stopping point','compare',[
    'DO IN THIS COURSE\nWrite and test the circuit. Generate a layout, inspect the checks and archive matching artifacts.',
    'LATER MANUFACTURING\nChoose an approved funded route, create an order and explicitly submit an accepted revision.'
], 'Tiny Tapeout provides an open preparation flow, but manufacturing and delivery are separately costed. The file package called tt_submission is an artifact generated by Actions; its name does not mean a fabrication order has been placed. This exercise ends when the source revision, tests, datasheet, layout and relevant reports are checked and archived. The final chapters explain how an approved order and revision submission would proceed, and how combined layout data eventually becomes structures on a wafer. Do not enter payment details or start an order to complete the learning exercise. Codespaces is optional and has separate compute and storage quotas, including storage while stopped; it is not required for this browser route. The current prices in this deck are dated calculator estimates rather than quotes or guarantees.',heading='Where the free route ends',check='A generated layout is a file; ordering and submitting for manufacture are separate actions.')
add('F06','Read each step as a small experiment','explain',[
    'WHY: understand what the step achieves.',
    'DO: follow the action or predict the example.',
    'CHECK: look for observable evidence of success.',
    'If it fails, identify the first useful error before continuing.'
], 'The deck is intended to support active learning. Before clicking a button, know what it changes; before running a tool, predict the result it should produce. After the action, inspect a specific file, state or result rather than assuming success from the absence of an error dialog. The bottom check on each practical slide tells you what observation is relevant. Screenshots identify the source and the feature to look for. Some controls require a signed-in account, so those pictures come from credited official documentation and may show older example repositories. Current counter, result and waveform captures are separately identified as actual evidence. The speaker notes contain deeper teaching explanations, manual section references and source URLs. The PDF contains the slides; use the PowerPoint or Word manual for the longer notes. If an image shows the reference account, substitute your own project in your browser.',heading='Read these conventions once',check='You can explain what a step should produce before doing it.')
add('F07','Keep the example and your version distinct','compare',[
    'REFERENCE\nRepository: tt-sky130-counter\nBranch: worked-example\nVerified commit: 61ef06b',
    'YOUR PROJECT\nYour account and repository\nYour own saved commit\nYour runs must test that same commit'
], 'The reference counter belongs to mdkamrulislam-web and was verified at the full SHA 61ef06bed008e76000f9ae46d65182e476d15dd6. Its reviewed branch is worked-example; main may still contain the initial template until its pull request is merged. Pinned links in the notes avoid this ambiguity. Your own copy will have a different repository name and different commit IDs even if the example files are identical. A commit is a saved version of the files; a branch is a named line of those versions. The same-commit rule matters because an older successful workflow does not prove newer edits are correct. Save the exact commit and run URLs with each evidence download. The original empty-template metadata failures are real failures of project information, not deliberately generated test assertion failures.',heading='Read these conventions once',check='Each result you trust belongs to the exact source version you intend to review.')
add('F08','Use the seven-file starter correctly','flow',[],
    'First create your own repository using the official SKY Verilog template. Its remaining files provide the automatic workflows, configuration, licences and test dependencies. Then extract the seven-file starter ZIP, inspect its directory tree and upload its contents at the new repository root. There must be no extra enclosing starter-pack directory in the uploaded paths. The root info.yaml defines metadata and the design source list; src contains counter.v and project.v; test contains Makefile,tb.v and test.py; docs contains info.md. Preserve the original source notices when adapting the example. The starter checksums match the verified public counter commit byte for byte. A later slide walks through this upload with official screenshots. This overview simply establishes which part comes from the template and which part describes the lesson circuit.',heading='Keep these companion files together',flow=[{'name':'Official template','detail':'Workflows, dependencies and process settings'},{'name':'Seven-file ZIP','detail':'Counter RTL, wrapper, test and datasheet text'},{'name':'Your saved project','detail':'A complete example on one reviewed commit'}],check='The ZIP supplements the template; preserve both the paths and template infrastructure.')

parts=[]
for name in ['beginner-concepts.json','beginner-browser.json','beginner-physical.json']:
    parts+=json.loads((HERE/name).read_text(encoding='utf-8'))
# Focused native crops make real code and viewer controls readable on a screen.
metadata=next(s for s in parts if s['id']=='B18')
metadata_names=deepcopy(metadata)
metadata_names.update(id='B18T',title='Step 7: read title, author and description',
    crop=[.440,.264,.012,.590],
    body=['These fields identify the circuit and credit its author.',
          'Describe the implemented behaviour; keep the supplied YAML indentation.'],
    caption='Native detail from the actual counter info.yaml at 61ef06b: title, author and description.')
parts.insert(parts.index(metadata),metadata_names)
metadata.update(title='Step 7: confirm the clock target and tile size',
    crop=[.440,.410,.012,.465],
    body=['clock_hz = 50000000 means 50 MHz, or a 20 ns cycle.',
          'tiles = 1x1 sets one layout tile for this example.',
          'Keep the clock metadata, test clock and timing constraints consistent.'],
    caption='Native detail from the actual counter info.yaml at 61ef06b: clock_hz and tiles.')
for slide_id,crop in {
    'B21':[.452,.773,.215,.046],
    'B23':[.497,.542,.130,.285],
    'B27':[0,.252,.210,.511],
    'B44':[.025,.301,.260,.560],
}.items():
    next(s for s in parts if s['id']==slide_id)['crop']=crop
viewer=next(s for s in parts if s['id']=='B40')
keys=deepcopy(viewer)
keys.update(id='B40K',title='Step 12: read the viewer’s keyboard controls',
    crop=[0,.031,.825,.900],
    body=['Read the actual KEYS panel: 1 hides fill, decap and tap cells.',
          'The other keys hide top geometry, isolate a selection or zoom to it.'],
    caption='Native crop of the actual viewer’s KEYS panel; display choices do not change the layout file.')
settings=deepcopy(viewer)
settings.update(id='B40V',title='Step 12: find the Filler cells checkbox',
    crop=[.799,0,.009,.855],
    body=['Expand Controls, then View Settings.',
          'Uncheck Filler cells to inspect the logic with the grouped support cells hidden.',
          'The checked Top cell geometry control keeps the top-level shape visible.'],
    caption='Native crop of the actual viewer’s View Settings; the unchecked Filler cells control is visible.')
idx=parts.index(viewer)+1
parts[idx:idx]=[keys,settings]
# Native PowerPoint crops magnify two actual datasheet paragraphs. Preserve the
# original image bytes and record the crop rectangles in the per-slide manifest.
datasheet=next(s for s in parts if s['id']=='B36')
datasheet['title']='Step 10: read reset and enable in the datasheet'
datasheet['crop']=[.10,.245,.10,.640]
datasheet['body']=['Read how reset and enable affect count at a rising edge.',
                   'Compare these words with the RTL and the top-level pin names.']
datasheet['caption']='Native crop of the actual generated datasheet, page 1; reference docs run 37693100755.'
wrap=dict(datasheet)
wrap.update(id='B36W',title='Step 10: check the flag description against the code',crop=[.10,.360,.10,.556],
    body=['The flag is high at count 255 while enable is high, before the overflow edge.',
          'Its combinational behaviour must agree with both the RTL and your test.'],
    check='Documentation explains the circuit; passing simulation verifies the tested behaviour.')
parts.insert(parts.index(datasheet)+1,wrap)
exercises=[]
start=text.index('## 12. Exercises with worked answers')
end=text.index('## 13. A readiness check',start)
chunk=text[start:end]
for i,m in enumerate(re.finditer(r'### Exercise (\d+): ([^\n]+)\n\n(.*?)(?=\n### Exercise |\Z)',chunk,re.S),1):
    number,title,body=m.groups();question,answer=body.split('**Answer:**',1)
    clean=lambda s: re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',s.replace('`','').replace('**','')).strip()
    question=clean(question);answer=clean(answer)
    short_title='Diagnose a hypothetical mismatch' if i==9 else title
    exercises.append(dict(id=f'E{i:02}Q',section='Worked exercises',title=f'Exercise {number}: {short_title}',layout='explain',body=[question],
      example='Predict it first.\nThen advance for the worked answer.',
      notes='Try the question before advancing to its answer. Return to the earlier circuit, wrapper or verification lesson to justify each step.\n\nQUESTION\n'+question+'\n\nWORKED ANSWER\n'+answer,
      guide_heading=f'Exercise {number}: {title}',sources=[SOURCE]))
    sentences=re.split(r'(?<=[.!?])\s+',answer)
    chunks=[];current=''
    for sentence in sentences:
        if current and len(current+' '+sentence)>200:chunks.append(current);current=sentence
        else:current=(current+' '+sentence).strip()
    if current:chunks.append(current)
    # Long worked answers continue on another slide rather than shrink the text.
    for part in range(0,len(chunks),3):
        exercises.append(dict(id=f'E{i:02}A{part//3+1}',section='Worked exercises',title=f'Answer {number}: {short_title}'+(' (continued)' if part else ''),layout='explain',body=chunks[part:part+3],
          notes='WORKED ANSWER\n'+answer+'\n\nConnect the answer to the specified behaviour and identify the evidence that would check it.',
          guide_heading=f'Exercise {number}: {title}',sources=[SOURCE]))
endings=[dict(id='Z01',section='Finish and review',title='Explain the result before calling it finished',layout='explain',body=[
    'Predict reset, count, hold, overflow and the pre-overflow wrap flag.',
    'Show matching source, test, documentation and layout evidence.',
    'Distinguish simulation, timing analysis, layout checks and silicon tests.',
    'Archive the checked revision before considering a fabrication order.'
],check='Demonstrate the circuit and explain what each form of evidence proves.',notes='Use these outcomes as the closing discussion. The original reference has successful RTL and documentation workflows, and its GDS workflow completed gds,precheck,gl_test and viewer. Those results belong to the pinned source revision. They support a checked design package and do not represent fabricated-silicon measurements. A learner should explain the subtle terminal-count flag and the enable/reset priorities, not merely point to a green icon. The instructor should review evidence organisation and ask a learner to identify what would need to change for a modified specification. A beginner usability trial and supervisor feedback remain separate from the technical and visual review completed for this course.',guide_heading='4.6 Demonstrate understanding before extending the design',sources=[SOURCE]),
dict(id='Z02',section='Finish and review',title='Choose a small next design change',layout='explain',body=[
    'Count down: specify whether zero wraps to 255.',
    'Parallel load: specify its pins and reset/load/enable priority.',
    'Update RTL, the independent model, metadata and datasheet together.',
    'Inspect the new commit’s tests, checks and cell measurements.'
],example='Change the specification first.\nThen change the implementation and its checks.',check='Old screenshots do not prove a modified circuit works.',notes='An extension is useful only if its expected behaviour is written before the code is changed. The counter is small enough for countdown or parallel-load changes, but either modification changes the model and boundary cases. For a countdown circuit, decide whether zero underflows to255 and what wrap means; do not reuse an up-counter terminal flag without evaluating the new specification. A load input needs chosen data pins and clear priority relative toreset and enable. Preserve the fixed Tiny Tapeout interface and update the unique top name in all three required locations if giving the design a new identity. After committing, inspect all relevant workflows for that new commit and archive its artifacts. The original example’s results remain the reference for the original design only.',guide_heading='Step 17 — Make a small extension after the example passes',sources=[SOURCE,'https://tinytapeout.com/hdl/important/']),
dict(id='Z03',section='Finish and review',title='Keep the learning package together',layout='explain',body=[
    'PowerPoint: editable diagrams, notes and linked sources.',
    'Course PDF: stable slide layout for reading and printing.',
    'Word/PDF manual: deeper explanations and the complete source appendix.',
    'Starter ZIP and original artifacts: exact source bytes and real evidence.'
],check='Use the full package when teaching or reproducing the lesson.',notes='The slides form the complete teaching sequence, while the manual is the longer reference for a learner who wants additional explanation or exact source listings. Both are grounded in the same counter revision. Use the ZIP to create the files because printed code can wrap visually, and retain source notices. Keep the unchanged FST,XML and metrics CSV alongside their run identity to distinguish native observations from instructional diagrams. Per-slide source metadata records the guide section and primary URLs; each screenshot also inherits its source category,date and checksum from the guide manifest. Some account-only controls are official documentation examples rather than screenshots of this account operating them. No fabrication order,payment or submitted revision occurred. Review with an actual beginner to assess teaching usability and duration.',guide_heading='Keep these companion files together',sources=[SOURCE,'https://tinytapeout.com/hdl/templates/'])]
course=front+parts+exercises+endings
targets=['C01','C26','B01','P01','P25','P35']
starts=[next(i for i,s in enumerate(course,1) if s['id']==target) for target in targets]
for i,(stage,target,start) in enumerate(zip(front[2]['flow'],targets,starts)):
    stop=starts[i+1]-1 if i+1<len(starts) else len(course)
    stage.update(target_id=target,range=f'Slides {start}–{stop}')
assert len({s['id']for s in course})==len(course)
for s in course:
    assert s['layout']in['cover','explain','code','bits','trace','flow','exercise','compare','screenshot'],s
    assert s['sources'] and s['notes'] and s['guide_heading'],s['id']
    if s.get('image'):assert(GUIDE/'img'/s['image']).is_file(),s['image']
(HERE/'beginner-course.json').write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'slides':len(course),'sections':list(dict.fromkeys(s['section']for s in course)),'notes_words':sum(len(s['notes'].split())for s in course)},indent=2))
