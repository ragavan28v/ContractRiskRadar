"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FileText, Gauge, ShieldCheck } from "lucide-react";
import clsx from "clsx";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: Gauge },
  { href: "/contracts", label: "Contracts", icon: FileText },
  { href: "/analytics", label: "Risk Analytics", icon: ShieldCheck }
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-64 flex-col border-r border-slate-200 bg-white/70 p-4 shadow-sm backdrop-blur dark:border-slate-800 dark:bg-slate-900/80 md:flex">
      <div className="mb-8">
        <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
          Contract Risk Radar
        </div>
        <div className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          AI Legal Risk Intelligence
        </div>
      </div>
      <nav className="space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition",
                active
                  ? "bg-primary-50 text-primary-600 dark:bg-primary-500/10 dark:text-primary-200"
                  : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
              )}
            >
              <Icon className="h-4 w-4" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}

