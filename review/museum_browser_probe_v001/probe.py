#!/usr/bin/env python3
"""Wanfo museum public page browser feasibility check; no circumvention or image redistribution.

Only a SINGLE accessible website pass. Screenshots remain temporary GitHub Actions artifacts
not committed to public repo. Public commit contains JSON metadata, hashes and gate outcomes.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse
from playwright.sync_api import sync_playwright, TimeoutError as BrowserTimeout

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"
PRIVATE=ROOT/"screenshots_for_short_retention_artifact"
OUT.mkdir(parents=True,exist_ok=True)
PRIVATE.mkdir(parents=True,exist_ok=True)
SITE="https://szbwgvue.chwhyun.cn/wanfodian/"
TARGETS=["结构","铺作","柱头铺作","栱端方直","卷杀","栌斗","华栱"]
KEYPHRASES=["柱头铺作","前后檐和两山位置的柱头铺作","栱端方直"]
report={
  "source":SITE,
  "test_date_utc":datetime.now(timezone.utc).isoformat(),
  "scope":"public site single-visit browser feasibility, no model extraction",
  "browser":"Chromium headless Playwright",
  "page_reached":False,
  "page_title":None,
  "nav_http_status":None,
  "target_text_found":[],
  "target_text_visible":[],
  "site_media_images_total":0,
  "site_media_images_loaded":0,
  "near_target_media_loaded":0,
  "near_target_media_examples":[],
  "same_instance_east_front_column_head":"NOT_PROVEN",
  "3d_network_candidate_urls":[],
  "canvas_count":0,
  "iframe_count":0,
  "screenshots":[],
  "navigation_errors":[],
  "console_errors":[],
  "gate":"NOT_RUN",
  "reason":"",
  "data_limits":[
     "Photos do not establish exact first-jump member identity",
     "Museum captions are not A1/A2 dimensional truth",
     "Only source URLs/hashes; screenshot bytes are NOT committed to public repository",
     "No source 3D assets downloaded or bypassed"
  ]
}
def save():
    for p in PRIVATE.glob("*.png"):
        payload=p.read_bytes()
        report["screenshots"].append({"filename":p.name,"bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest()})
    (OUT/"MUSEUM_BROWSER_PROBE.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def safe_url(raw):
    try:
        u=urlparse(raw)
        if u.scheme not in ("https","http"):return ""
        # Remove query, fragment to avoid accidental tokens.
        return urlunparse((u.scheme,u.netloc,u.path,"","",""))
    except Exception:return ""

def shoot(page,name):
    try:
        p=PRIVATE/(name+".png")
        page.screenshot(path=str(p),full_page=False,animations="disabled",timeout=14000)
        return True
    except Exception as e:
        report["navigation_errors"].append("screenshot-"+name+": "+str(e)[:300])
        return False

try:
  with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=["--no-sandbox"])
    context=browser.new_context(viewport={"width":1365,"height":920},device_scale_factor=1,locale="zh-CN",
                                java_script_enabled=True,ignore_https_errors=False)
    page=context.new_page()
    page.set_default_timeout(7000)
    requests=[]
    def on_response(resp):
        url=safe_url(resp.url)
        if re.search(r"\.(glb|gltf|bin|obj|fbx|ktx2|splat)(?:$)",url,re.I):
            if len(requests)<80:requests.append({"url":url[:300],"status":resp.status,"content_type":resp.headers.get("content-type","")[:80]})
    def on_console(msg):
        if msg.type=="error" and len(report["console_errors"])<12:
            report["console_errors"].append(msg.text[:250])
    page.on("response",on_response)
    page.on("console",on_console)
    try:
        nav=page.goto(SITE,wait_until="domcontentloaded",timeout=37000)
        report["nav_http_status"]=nav.status if nav else None
        report["page_reached"]=bool(nav and 200<=nav.status<400)
    except Exception as e:
        report["navigation_errors"].append("navigate: "+str(e)[:650])
        # A timeout can still yield a visually useful page.
    try:page.wait_for_timeout(3500)
    except Exception:pass
    try:report["page_title"]=page.title()[:200]
    except Exception:pass

    try:
        data=page.evaluate("""() => {
            const body=document.body;
            const text=(body?.innerText||'');
            const imgs=[...document.images].map((im,i)=>{
              const b=im.getBoundingClientRect();
              return {
               id:i, src:im.currentSrc || im.src || '', alt:(im.alt||'').slice(0,160),
               naturalWidth:im.naturalWidth,naturalHeight:im.naturalHeight,
               displayWidth:Math.round(b.width), displayHeight:Math.round(b.height),
               absoluteTop:Math.round(b.top+scrollY),absoluteLeft:Math.round(b.left+scrollX),
               loaded:im.complete && im.naturalWidth>0,
               visible:b.width>=70 && b.height>=50
              };
            });
            const nodes=[...document.querySelectorAll('h1,h2,h3,h4,p,div,span,button,a')];
            const targetNodes=nodes.filter(n=>
                n.children.length===0 && /^(柱头铺作|铺作|卷杀|栱端方直|结构)$/.test((n.textContent||'').trim())
              ).slice(0,100).map(n=>{
                 const b=n.getBoundingClientRect();
                 return {text:(n.textContent||'').trim(),tag:n.tagName,absoluteTop:Math.round(b.top+scrollY),
                    width:Math.round(b.width),height:Math.round(b.height),
                    clickable:['A','BUTTON'].includes(n.tagName) || n.getAttribute('role')==='button'};
              });
            return {textSample:text.slice(0,12000),imgs,targetNodes,canvasCount:document.querySelectorAll('canvas').length,
               iframeCount:document.querySelectorAll('iframe').length,documentHeight:document.documentElement.scrollHeight};
        }""")
    except Exception as e:
        data={"textSample":"","imgs":[],"targetNodes":[],"canvasCount":0,"iframeCount":0}
        report["navigation_errors"].append("extract-dom: "+str(e)[:400])
    text=data.get("textSample","")
    report["page_visible_text_sample_chars"]=len(text)
    report["target_text_found"]=[s for s in TARGETS if s in text]
    report["target_text_visible"]=[a for a in KEYPHRASES if a in text]
    report["canvas_count"]=data.get("canvasCount",0)
    report["iframe_count"]=data.get("iframeCount",0)
    img=data.get("imgs",[])
    report["site_media_images_total"]=len(img)
    report["site_media_images_loaded"]=sum(1 for x in img if x["loaded"] and x["naturalWidth"]>=220)
    report["visible_text_sample"]=re.sub(r"\s+"," ",text)[:1100]
    report["target_nodes"]=data.get("targetNodes",[])[:30]
    report["navigation_3d_responses"]=requests[:20]

    shoot(page,"01_website_initial_view")
    # Seek relevant section. Scroll is based on page DOM, no need for manual screenshots.
    hits=[x for x in data.get("targetNodes",[]) if x["text"]=="柱头铺作" and x["height"]>0]
    if not hits:
        hits=[x for x in data.get("targetNodes",[]) if x["text"]=="铺作" and x["height"]>0]
    if hits:
        y=max(0,hits[0]["absoluteTop"]-180)
        try:
            page.evaluate("(y)=>window.scrollTo(0,y)",y)
            page.wait_for_timeout(1500)
            shoot(page,"02_target_columnhead_section")
        except Exception as e:report["navigation_errors"].append("scroll-target: "+str(e)[:300])
        # Refresh image loading after scroll: lazy-loaded images may not exist at initial viewport.
        try:
            refreshed=page.evaluate("""() => [...document.images].map((im,i)=>{const b=im.getBoundingClientRect();return {
                id:i,src:im.currentSrc||im.src||'',alt:(im.alt||'').slice(0,160),
                naturalWidth:im.naturalWidth,naturalHeight:im.naturalHeight,
                absoluteTop:Math.round(b.top+scrollY),loaded:im.complete&&im.naturalWidth>0};})""")
            img=refreshed
            report["site_media_images_loaded"]=sum(1 for x in img if x["loaded"] and x["naturalWidth"]>=220)
        except Exception as e:report["navigation_errors"].append("refresh-lazy-images: "+str(e)[:300])
        # Proximity is not proof that an image depicts the exact member.
        candidates=sorted((x for x in img if x["loaded"] and x["naturalWidth"]>=220),
                          key=lambda x:abs(x["absoluteTop"]-hits[0]["absoluteTop"]))
        near=[x for x in candidates if abs(x["absoluteTop"]-hits[0]["absoluteTop"])<=1400]
        report["near_target_media_loaded"]=len(near)
        report["near_target_media_examples"]=[{
          "url_without_query":safe_url(x["src"])[:380],
          "natural_width":x["naturalWidth"],"natural_height":x["naturalHeight"],
          "relative_y_px":x["absoluteTop"]-hits[0]["absoluteTop"],"alt":x["alt"]
        } for x in near[:12]]
    # A secondary section view, if present, for morphology.
    other=[x for x in data.get("targetNodes",[]) if x["text"] in ("卷杀","栱端方直") and x["height"]>0]
    if other:
        try:
            page.evaluate("(y)=>window.scrollTo(0,y)",max(0,other[0]["absoluteTop"]-180))
            page.wait_for_timeout(1000)
            shoot(page,"03_gong_terminal_section")
        except Exception as e:report["navigation_errors"].append("scroll-second: "+str(e)[:300])

    # No automatic click/asset scraping: a single page and nearby section are enough for G0.
    if report["page_reached"] and "柱头铺作" in report["target_text_found"] and report["near_target_media_loaded"]>0:
        report["gate"]="PASS_AUTO_CAPTURE_SECTION"
        report["reason"]="Reached public page; column-head section and nearby loaded image(s) auto-captured. Exact individual member identity remains NOT PROVEN."
    elif report["page_reached"] and ("柱头铺作" in report["target_text_found"] or "铺作" in report["target_text_found"]):
        report["gate"]="PARTIAL_TEXT_ONLY"
        report["reason"]="Relevant section text accessible, but no suitable linked image was captured/confirmed."
    else:
        report["gate"]="FAIL_AUTOMATED_BROWSER_REFERENCE"
        report["reason"]="Public page/target column-head could not be verified through browser DOM."
    browser.close()
except Exception as exc:
    report["gate"]="FAIL_AUTOMATED_BROWSER_REFERENCE"
    report["reason"]="Browser or operating environment could not complete reproducible extraction."
    report["navigation_errors"].append(type(exc).__name__+": "+str(exc)[:800])
finally:
    save()
    print("WANFO_MUSEUM_PROBE_GATE",report["gate"])
    print("WANFO_MUSEUM_PAGE_HTTP",report["nav_http_status"])
    print("WANFO_MUSEUM_MEDIA",report["site_media_images_loaded"],"NEAR_TARGET",report["near_target_media_loaded"])
    print("WANFO_MUSEUM_RESULT_JSON",str(OUT/"MUSEUM_BROWSER_PROBE.json"))
