import type { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://www.xn--o80bk8isxeinax68f.com'

  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1.0,
    },
    {
      url: `${baseUrl}/search`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/sanction`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8,
    },
  ]

  const categories = [
    'unfair-dismissal',
    'unfair-discipline',
    'sexual-harassment',
    'verbal-physical-abuse',
    'embezzlement',
    'misconduct',
    'management-dismissal',
    'transfer',
    'renewal-expectation',
    'dismissal-nonexistence',
    'wage-dispute',
    'workplace-bullying',
    'probation',
    'retirement',
    'industrial-accident',
    'discrimination',
  ]

  const categoryPages: MetadataRoute.Sitemap = categories.map((cat) => ({
    url: `${baseUrl}/search?category=${cat}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }))

  return [...staticPages, ...categoryPages]
}
