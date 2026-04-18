import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()
  const accept = request.headers.get('accept') || ''

  // Content Signals header on all responses
  response.headers.set('Content-Signal', 'ai-train=yes, search=yes, ai-input=yes')

  // Markdown content negotiation
  if (accept.includes('text/markdown')) {
    // For markdown requests, add indicator header
    // The actual markdown conversion happens at page level
    response.headers.set('X-Markdown-Available', 'true')
    response.headers.set('Vary', 'Accept')
  }

  // Agent discovery headers
  response.headers.set('X-Robots-Tag', 'all')

  return response
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api routes (they have their own handling)
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
