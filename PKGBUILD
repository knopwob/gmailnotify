# Maintainer: Sascha Kruse <knopwob@googlemail.com>

_pkgname=gmailnotify
pkgname=gmailnotify-git
pkgver=20121130
pkgrel=1
pkgdesc="A gmail notifier using libnotify"
arch=('any')
url="https://github.com/knopwob/gmailnotify"
license=('GPL')
groups=()
depends=('python2' 'python2-notify')
optdepends=('tk: interactive password prompt')
makedepends=('git')

_gitroot="https://github.com/knopwob/${_pkgname}.git"
_gitname="${_pkgname}"

build() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [[ -d "$_gitname" ]]; then
    cd "$_gitname" && git pull origin
    msg "The local files are updated."
  else
    git clone "$_gitroot" "$_gitname"
  fi

  msg "GIT checkout done or server timeout"
  msg "Starting build..."

  rm -rf "$srcdir/$_gitname-build"
  git clone "$srcdir/$_gitname" "$srcdir/$_gitname-build"
  cd "$srcdir/$_gitname-build"

}

package() {
  cd "$srcdir/$_gitname-build"
  mkdir -p $pkgdir/usr/bin
  install -Dm 755 gmailnotify.py $pkgdir/usr/bin/
}

# vim:set ts=2 sw=2 et:
