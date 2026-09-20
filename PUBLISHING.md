# Publishing AICD

This file lists the steps of publishing this document that the repository cannot perform for itself, because each one needs an account that belongs to the author: GitHub, Zenodo, or the registrar holding a domain name. Nothing in this file has been done automatically, and no script in this repository does any of it; every item below is still waiting.

The reader assumed here is the author, working on their own machine, already signed in to GitHub in the browser and already able to push to the repository from the command line. Work through the sections in the order given under "Order of operations" at the end, and tick the numbered items off as they are done.

## 1. Enable GitHub Pages

The site is published by a workflow rather than from a branch, so Pages has to be told to take its content from GitHub Actions. This is a one time setting.

1. Open https://github.com/rachidsahane/AICD-METHODOLOGY in the browser.
2. Click **Settings** in the row of tabs across the top of the repository page.
3. Click **Pages** in the left sidebar, under the "Code, planning, and automation" group.
4. Under the **Build and deployment** heading, open the **Source** dropdown and select **GitHub Actions**. The choice takes effect as soon as it is selected.

Once that is set, `.github/workflows/pages.yml` deploys the site on every push to `main`. A push that happened before Pages was enabled is not deployed retroactively, so the first deployment is started by hand:

5. Click the **Actions** tab at the top of the repository page.
6. In the list of workflows in the left sidebar, click **Deploy the document to GitHub Pages**.
7. Click the **Run workflow** button on the right of the bar that appears, leave the branch set to `main`, and click the green **Run workflow** button inside the dropdown.
8. Wait for the run to finish with a green check. The first run also has to register the Pages deployment, so it can take a few minutes.

Confirm it worked:

9. Open https://rachidsahane.github.io/AICD-METHODOLOGY/ . If the address returns 404 for a minute or two after a successful run, reload; the first deployment is not served instantly.
10. Check the cover image at the top of the page. It is the generated background `src/cover_bg.jpg`, set as the CSS background of the cover block, so it must fill that block edge to edge. Because it is a background rather than an image element, a file that failed to load leaves the pale panel colour showing instead of a broken image icon, so a blank band where the cover should be is the symptom to look for.
11. Scroll to the "About the author" block near the end of the page and check the round author portrait, `src/portrait_circle.png`, renders there.

If either image is missing while the text is fine, the deployment published the HTML without the files next to it. Open the failing run from the **Actions** tab, read its log, and confirm the workflow copied the whole of `src/` into the artifact it uploaded. Before investigating anything else, force a reload with Shift and the reload button, which rules out a cached earlier attempt.

## 2. Create and push the tag v0.3, then verify the release

**Do not push the tag before the publication branch has been merged into `main`.** `.github/workflows/release.yml` builds whatever commit the tag points at, so a tag created on an unmerged branch, or on an older commit, produces a release whose PDF is not the published document. Recovering from that means deleting the release and the tag and starting the section again.

1. Merge the publication pull request into `main` and confirm on the repository page that `main` now contains the release workflow, the build script and the document source.
2. Bring the local clone to that commit:

   ```sh
   git checkout main
   git pull origin main
   ```

3. Create the annotated tag:

   ```sh
   git tag -a v0.3 -m "AICD v0.3"
   ```

4. Push the tag, which is what starts the release:

   ```sh
   git push origin v0.3
   ```

5. Watch the build. Click the **Actions** tab; a new run appears within a few seconds, triggered by the tag. It installs the pinned build dependencies, runs `build/build.sh`, and creates the release with the built PDF attached. If it fails, open the run and read the step that went red; the build fails loudly and early when a referenced image is missing from `src/`.
6. Open https://github.com/rachidsahane/AICD-METHODOLOGY/releases/latest and check the release is the one just built, tagged `v0.3`.
7. Read the release notes on that page against the `0.3` entry in `CHANGELOG.md`. The notes come from that entry and must match it; if they do not, the tag points at a commit that predates the entry.
8. Check that `AICD-Methodology-v0.3.pdf` is listed under **Assets** on the release.
9. Download that file, open it, and confirm it is the finished document: the cover renders, the colophon follows it, and the author page carries the portrait.
10. Confirm the page count is 76. In a PDF viewer this is the last page number; from a terminal, in the directory the file was downloaded to:

    ```sh
    python3 -c "from pypdf import PdfReader; print(len(PdfReader('AICD-Methodology-v0.3.pdf').pages))"
    ```

    The expected output is `76`. A different number means the file that was built is not the document this release is meant to carry, most often because the machine that built it lacked the fonts the document expects, which changes the pagination; see `build/fonts.md`.

If something is wrong and the release has to be redone, delete the release first, with the **Delete** control on the release page, then remove the tag from both places and start again from step 3:

```sh
git push origin :refs/tags/v0.3
git tag -d v0.3
```

## 3. Connect the repository to Zenodo so a DOI is minted

Zenodo archives GitHub releases and mints a DOI for each archived release, which is what makes the document citable in academic work.

1. Go to https://zenodo.org .
2. Click **Log in** at the top right of the page.
3. Choose **Log in with GitHub**.
4. Authorise Zenodo when GitHub asks it to confirm access.
5. Open https://zenodo.org/account/settings/github/ .
6. Find `rachidsahane/AICD-METHODOLOGY` in the list of repositories on that page. If it is not listed, use the **Sync now** control at the top of the page and reload.
7. Switch the toggle beside that repository to **On**.

The ordering matters and is the one thing that is easy to get wrong. Zenodo only archives releases created **after** the toggle is switched on. It does not reach back for releases that already exist. So either switch the toggle on before section 2, which is the simple path and the one recommended under "Order of operations" below, or, if the v0.3 release already exists by the time Zenodo is connected, switch the toggle on and then publish a further release, for example `v0.3.1`, because only that later release gets a DOI.

Once a release has been archived, Zenodo shows its DOI on the repository's row on that same settings page and on the Zenodo record itself. Zenodo mints a version DOI for each archived release and a concept DOI that always resolves to the newest version. Use the concept DOI in the citation files, so the citation stays correct across later releases.

The DOI then has to be pasted into three files by hand. Each place carries a marker that is replaced:

1. `README.md`, in the "How to cite" section. Replace `<<NEEDS: Zenodo DOI after first archived release>>` with the DOI. The marker occurs twice, once in the APA citation and once in the `doi` field of the BibTeX entry, and both have to be replaced.
2. `CITATION.cff`. Uncomment the `identifiers` block at the end of the commented note, that is, remove the leading `# ` from its four lines while keeping the indentation exactly as the comment shows it, and replace `<<NEEDS: Zenodo DOI after first archived release>>` with the DOI.
3. `src/AICD_Methodology_v0.3.html`, the document source behind the colophon. The `dc.identifier` meta tag sits in the `head`, just above the `title` element, inside an HTML comment. Remove the comment markers so the tag is live, and replace `<<NEEDS: DOI>>` with the DOI.

That third edit changes the document itself, so the PDF built before it does not carry the DOI. After editing the HTML, rebuild:

```sh
python3 -m pip install -r build/requirements.txt
build/build.sh
```

and then cut a new release, following section 2 with the new version number, so the PDF attached to the latest release is the one that carries the DOI. A tag that already exists is not moved to do this; a new tag is created.

## 4. Replace the author portrait

`src/portrait_circle.png` is currently a generated monogram placeholder, not a photograph. It is a teal disc carrying the letters A and S, produced by `build/generate_assets.py` because no portrait file was present when the repository was assembled. It exists so the document builds and paginates correctly, and it is meant to be replaced.

To use a real photograph:

1. Prepare a square image, at least 700 by 700 pixels. The placeholder is 1000 by 1000, which is a good target. Keep the face centred, because the file is displayed clipped to a circle and the corners are cut away.
2. Save it, as PNG, over `src/portrait_circle.png`. Keep the file name and the location, because that is the path the document references. Do not run `build/generate_assets.py` again once the photograph is in place: it rewrites `src/portrait_circle.png` with the monogram every time it runs, and would put the placeholder back.
3. Rebuild the PDF:

   ```sh
   python3 -m pip install -r build/requirements.txt
   build/build.sh
   ```

4. Open `dist/AICD-Methodology-v0.3.pdf` at the author page and check the photograph is round and framed by the teal border.
5. Cut a new release, following section 2, so the published PDF carries the photograph.

No markup change is needed. The stylesheet rule for `.authorpage .photo img` fixes the size at 58mm by 58mm, sets `border-radius: 50%` and draws the teal border, so any square file is clipped and framed the same way.

A photograph, and the author's likeness in it, are excluded from the CC BY 4.0 license and remain all rights reserved. The colophon, the author page footer, the `dc.rights` meta tag in the document source and the license section of `README.md` all state this already, so replacing the image file requires no change to any license text.

## 5. If a custom domain is acquired

Nothing in the repository assumes a custom domain, and the GitHub Pages address keeps working if one is never bought. These steps apply only if a domain is acquired and is to serve the document.

1. Create the DNS records at the registrar or DNS provider that holds the domain, before touching GitHub. Which records depend on the kind of name:

   For an apex domain, that is a bare name such as `example.com`, create four **A** records on the zone root, usually written as `@`, one for each of these addresses:

   ```
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```

   For a subdomain, such as `www.example.com` or `aicd.example.com`, create a single **CNAME** record for that host pointing to:

   ```
   rachidsahane.github.io
   ```

   The CNAME target is the account's Pages domain and carries no repository name and no path.

2. Open the repository, click **Settings**, then **Pages** in the left sidebar.
3. Under **Custom domain**, type the domain and click **Save**.
4. GitHub runs a DNS check on the domain and reports the result under the field. DNS changes can take up to 24 hours to propagate, so a check that fails immediately after the records were created is not conclusive; wait and reload the page. The records can be inspected independently with `dig +short example.com` for an apex domain, which should return the four addresses above, or `dig +short www.example.com`, which should return the `rachidsahane.github.io` target.
5. When the DNS check has passed, tick **Enforce HTTPS** on the same page. The certificate is issued automatically and can take up to 24 hours to become available, so the checkbox may be greyed out at first.

Once the domain serves the document, three files carry addresses that have to be updated by hand:

1. `README.md`, the Site link under "Read it".
2. `CITATION.cff`, the `url` field. Leave `repository-code` pointing at https://github.com/rachidsahane/AICD-METHODOLOGY , because that field names where the source lives, not where the document is read.
3. `src/AICD_Methodology_v0.3.html`, the colophon near the front of the document, where the repository address is printed for the reader. Editing it changes the document, so rebuild the PDF with `build/build.sh` and cut a new release afterwards, following section 2.

## 6. Trademark registration

Registration of the mark AICD through OAPI, the African Intellectual Property Organization, of which Cameroon is a member state, is the author's decision alone. It is not automated anywhere in this repository, and no step in this file depends on it. `TRADEMARK.md` sets out how the name may and may not be used, and it applies whether or not the mark is ever registered. Questions about the mark, and requests for permission to use it, go to rachidsahane007@gmail.com .

## Order of operations

1. Merge the publication pull request into `main`, so that `main` holds the document, the build and the workflows.
2. Enable GitHub Pages, section 1, and confirm the site renders with both images.
3. Switch the Zenodo toggle on, section 3, while no release exists yet, so the first release is archived and gets a DOI.
4. Create and push the tag `v0.3`, section 2, then verify the release and paste the DOI into the three files.
