"use client"

import Link from "next/link"
import { useState } from "react"
import { ChevronDown, ChevronRight } from "lucide-react"

interface SidebarItem {
  title: string
  href: string
  items?: SidebarItem[]
}

const sidebarItems: SidebarItem[] = [
  {
    title: "Introdução",
    href: "#introducao",
    items: [
      { title: "Visão Geral", href: "#visao-geral" },
      { title: "Quick Start", href: "#quick-start" },
      { title: "Autenticação", href: "#autenticacao" },
    ]
  },
  {
    title: "Recursos",
    href: "#recursos",
    items: [
      { title: "Consulta de CNPJ", href: "#consulta-cnpj" },
      { title: "Rate Limits", href: "#rate-limits" },
      { title: "Respostas", href: "#respostas" },
    ]
  },
  {
    title: "API Reference",
    href: "#api-reference",
    items: [
      { title: "Endpoints", href: "#endpoints" },
      { title: "Códigos de Erro", href: "#erros" },
    ]
  },
  {
    title: "Exemplos",
    href: "#exemplos",
    items: [
      { title: "Python", href: "#python" },
      { title: "JavaScript", href: "#javascript" },
      { title: "PHP", href: "#php" },
    ]
  },
]

export function Sidebar() {
  const [openSections, setOpenSections] = useState<Set<string>>(new Set(["Introdução"]))

  const toggleSection = (title: string) => {
    const newOpenSections = new Set(openSections)
    if (newOpenSections.has(title)) {
      newOpenSections.delete(title)
    } else {
      newOpenSections.add(title)
    }
    setOpenSections(newOpenSections)
  }

  return (
    <aside className="w-64 bg-gray-950 border-r border-gray-800 h-screen sticky top-0 overflow-y-auto">
      <div className="p-6">
        <Link href="/" className="text-xl font-bold text-emerald-500 hover:text-emerald-400 transition">
          AuthBrasil CNPJ
        </Link>
        <p className="text-xs text-gray-400 mt-1">Documentação</p>
      </div>

      <nav className="px-3 pb-6">
        {sidebarItems.map((section) => (
          <div key={section.title} className="mb-4">
            <button
              onClick={() => toggleSection(section.title)}
              className="flex items-center justify-between w-full px-3 py-2 text-sm font-semibold text-gray-200 hover:bg-gray-800 rounded-lg transition"
            >
              <span>{section.title}</span>
              {section.items && (
                openSections.has(section.title) ? (
                  <ChevronDown className="w-4 h-4 text-emerald-500" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-gray-500" />
                )
              )}
            </button>
            
            {section.items && openSections.has(section.title) && (
              <div className="ml-3 mt-1 space-y-1">
                {section.items.map((item) => (
                  <a
                    key={item.href}
                    href={item.href}
                    className="block px-3 py-1.5 text-sm text-gray-400 hover:text-emerald-500 hover:bg-gray-800 rounded-lg transition"
                  >
                    {item.title}
                  </a>
                ))}
              </div>
            )}
          </div>
        ))}
      </nav>

      <div className="border-t border-gray-800 p-4">
        <a
          href="https://api.authbrasil.app.br/api/v1/docs"
          target="_blank"
          rel="noopener noreferrer"
          className="block text-sm text-gray-400 hover:text-emerald-500 transition"
        >
          📖 Swagger API Docs
        </a>
      </div>
    </aside>
  )
}
