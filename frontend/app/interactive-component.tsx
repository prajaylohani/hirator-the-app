"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Spinner } from "@/components/ui/spinner"
import {
  Field,
  FieldContent,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSeparator,
  FieldSet,
  FieldTitle,
} from "@/components/ui/field"
import {
  ChevronDownIcon,
  ArrowDown,
  CodeXml,
} from 'lucide-react';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"

export function InteractiveComponent() {
  const [currentFileName, setCurrentFileName] = useState('')
  const [previewContent, setPreviewContent] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [isLoadingYaml, setIsLoadingYaml] = useState(false);
  const [isLoadingTex, setIsLoadingTex] = useState(false);

  // reset form on refresh: does nothing, it resets by default
  // useEffect(() => { }, [])

  // file input change handler
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) {
      resetPreview()
      return
    }

    // store filename
    setCurrentFileName(file.name)

    // validate extension
    const ext = file.name.split('.').pop()?.toLowerCase()
    if (!['yaml', 'yml', 'tex'].includes(ext || '')) {
      alert('Please select YAML (.yaml, .yml) or TeX (.tex) file')
      resetPreview()
      if (fileInputRef.current) fileInputRef.current.value = ''
      return
    }

    // load preview
    const reader = new FileReader()
    reader.onload = (e) => {
      setPreviewContent(e.target?.result as string)
    }
    reader.readAsText(file)
  }

  // load sample
  const loadSample = async (sampleURL: string) => {
    try {
      const response = await fetch(sampleURL)
      if (!response.ok) throw new Error('Failed to load sample')
      const text = await response.text()
      setPreviewContent(text)
      setCurrentFileName('sample.yaml')
      if (fileInputRef.current) fileInputRef.current.value = ''
    } catch (error) {
      console.error('Error loading sample:', error)
      alert('Failed to load sample YAML')
    }
  }

  // remove extension from filename
  const getFileNameWithoutExtension = (fileName: string) => {
    return fileName.split('.').slice(0, -1).join('.')
  }

  const downloadSourceAs = (ext: string) => {
    if (!previewContent.trim()) {
      alert('No content to download')
      return
    }

    const filename = getFileNameWithoutExtension(currentFileName) || 'document'

    // create blob from textarea content
    const blob = new Blob([previewContent], { type: 'text/plain;charset=utf-8' })

    // create temporary download link
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename + '.' + ext

    // trigger download and cleanup
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const resetPreview = () => {
    setCurrentFileName('')
    setPreviewContent('')
  }

  // scroll to bottom button with auto disappear
  function ScrollToBottomButton() {
    const [isVisible, setIsVisible] = useState(false)

    useEffect(() => {
      const handleScroll = () => {
        const { scrollTop, scrollHeight, clientHeight } = document.documentElement
        setIsVisible(scrollTop + clientHeight < scrollHeight - 200)
      }

      window.addEventListener('scroll', handleScroll)
      handleScroll()
      return () => window.removeEventListener('scroll', handleScroll)
    }, [])

    if (!isVisible) return null

    const scrollToBottom = () => {
      window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
      })
    }

    return (
      <Button
        onClick={scrollToBottom}
        className="fixed bottom-6 right-6 z-50 h-12 w-12 rounded-full shadow-lg hover:shadow-xl transition-all duration-300"
        size="icon"
        aria-label="Scroll to bottom"
      >
        <ArrowDown className="h-5 w-5" />
      </Button>
    )
  }

  // set isLoadingYaml status for spinner
  const handleClickYaml = async () => {
    setIsLoadingYaml(true);
    // simulate async work: 1min timer same as tex compiler in flask
    await new Promise((r) => setTimeout(r, 30000));
    setIsLoadingYaml(false);
  };

  // set isLoadingTex status for spinner
  const handleClickTex = async () => {
    setIsLoadingTex(true);
    // simulate async work: 1min timer same as tex compiler in flask
    await new Promise((r) => setTimeout(r, 30000));
    setIsLoadingTex(false);
  };

  // the real thing
  return (
    <div className="flex min-h-svh w-full max-w-3xl flex-col gap-2 p-6 leading-loose mx-auto">

      {/* scroll to bottom button */}
      <ScrollToBottomButton />

      {/* heading */}
      <h1
        className="scroll-m-20 text-center text-4xl font-bold text-balance"
        onClick={() => {
          document.body.style.opacity = '0.7'
          setTimeout(() => window.location.reload(), 120)
        }}
      >
        hirator
      </h1>

      {/* source code link */}
      <Button
        variant="link"
        type="button"
      >
        <a
          href="https://github.com/prajaylohani/hirator-the-app"
          target="_blank"
          className="inline-flex items-center gap-2">
          <CodeXml data-icon="inline-start" />
          View Source Code
        </a>
      </Button>

      <form
        id="theForm"
        method="post"
        encType="multipart/form-data"
        action="/api/upload"
      >
        <FieldSet>
          <FieldGroup>
            <Field>
              {/* upload source */}
              <FieldLabel htmlFor="fileInput">
                Fill from source file (.yaml or .tex)
                <Badge variant="secondary" className="ml-auto">
                  Optional
                </Badge>
              </FieldLabel>

              {/* <FieldDescription> */}
              {/*   Select a source to upload */}
              {/* </FieldDescription> */}

              <Field className="flex flex-col gap-2 sm:flex-row" >
                <Input
                  id="fileInput"
                  ref={fileInputRef}
                  type="file"
                  accept=".yaml,.yml,.tex"
                  onChange={handleFileChange}
                  className="flex-auto"
                />

                {/* fill sample */}
                <Button
                  variant="secondary"
                  type="button"
                  className="flex-auto"
                  onClick={() => loadSample('/api/downloads/sample')}
                >
                  Or fill sample data
                </Button>
              </Field>

              {/* upload image */}
              <FieldLabel htmlFor="image">
                Select image file
                <Badge variant="secondary" className="ml-auto">
                  Optional
                </Badge>
              </FieldLabel>

              <Input
                type="file"
                id="image"
                name="image"
                accept="image/*"
              />

              {/* <FieldDescription> */}
              {/*   Select a picture to upload */}
              {/* </FieldDescription> */}

              {/* enter document name */}
              <FieldLabel htmlFor="filename">
                Enter document name
                <Badge variant="secondary" className="ml-auto">
                  Optional
                </Badge>
              </FieldLabel>

              <Input
                id="filename"
                name="filename"
                type="text"
                placeholder={currentFileName ? getFileNameWithoutExtension(currentFileName) : 'document'}
              />

              {/* <FieldDescription> */}
              {/*   Choose a name for your output document */}
              {/* </FieldDescription> */}

              {/* text area */}
              <FieldLabel htmlFor="preview">
                Document content
              </FieldLabel>

              {/* <FieldDescription> */}
              {/*   Write document contents */}
              {/* </FieldDescription> */}

              <Textarea
                id="preview"
                name="preview"
                rows={12}
                value={previewContent}
                onChange={(e) => setPreviewContent(e.target.value)}
                placeholder="Write document contents here..."
                maxLength={50000}
                required
              />

              <Field className="flex flex-col gap-2 sm:flex-row" >
                {/* submit buttons */}
                <Button
                  variant="default"
                  type="submit"
                  className="flex-auto"
                  name="action"
                  value="download_pdf"
                  disabled={!previewContent}
                  onClick={handleClickYaml}
                >
                  {isLoadingYaml && (
                    <Spinner data-icon="inline-start" />
                  )}
                  {isLoadingYaml ? "Generating PDF..." : "Download PDF"}
                </Button>

                <Button
                  variant="secondary"
                  type="button"
                  className="flex-auto"
                  onClick={() => downloadSourceAs('yaml')}
                  disabled={!previewContent}
                >
                  {/* <Spinner data-icon="inline-start" /> */}
                  Download source
                </Button>

                {/* reset button */}
                <Button
                  variant="destructive"
                  type="button"
                  className="flex-auto"
                  onClick={resetPreview}
                  disabled={!previewContent}
                >
                  Delete
                </Button>

              </Field>

              <FieldSeparator />

              {/* advanced tex */}
              <Collapsible className="rounded-md">
                <CollapsibleTrigger asChild>
                  <Button
                    variant="ghost"
                    type="button"
                    className="group w-full data-[state=open]:bg-transparent"
                    title="Use this only if you know LaTeX!"
                  >
                    <span>Advanced TeX</span>
                    <ChevronDownIcon className="ml-auto group-data-[state=open]:rotate-180" />
                  </Button>
                </CollapsibleTrigger>

                <CollapsibleContent className="flex min-w-0 flex-col gap-2 pt-0">
                  {/* <div> */}
                  {/*   Use this only if you know LaTeX! */}
                  {/* </div> */}

                  <Field className="flex flex-col gap-2 sm:flex-row" >
                    <Button
                      variant="default"
                      type="submit"
                      className="flex-auto"
                      name="action"
                      value="compile_tex"
                      disabled={!previewContent}
                      onClick={handleClickTex}
                    >
                      {isLoadingTex && (
                        <Spinner data-icon="inline-start" />
                      )}
                      {isLoadingTex ? "Generating PDF..." : "Download PDF"}
                    </Button>

                    <Button
                      variant="secondary"
                      type="button"
                      className="flex-auto"
                      onClick={() => downloadSourceAs('tex')}
                      disabled={!previewContent}
                    >
                      Download source
                    </Button>

                    <Button
                      variant="secondary"
                      type="submit"
                      className="flex-auto"
                      name="action"
                      value="yaml2tex"
                      disabled={!previewContent}
                    >
                      YAML to TeX
                    </Button>
                  </Field>
                </CollapsibleContent>
              </Collapsible>
            </Field>
          </FieldGroup>
        </FieldSet>
      </form>
    </div>
  )
}
