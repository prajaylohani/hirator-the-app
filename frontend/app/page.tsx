import type { Metadata } from 'next'
import { InteractiveComponent } from './interactive-component'

export const metadata: Metadata = {
  title: 'hirator',
  description: 'get hired.',
}

export default function Page() {
  return <InteractiveComponent />
}
